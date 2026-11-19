"""Aggregate actual runs without changing labels or excluding failures."""
import json
from pathlib import Path
from collections import Counter
import numpy as np


def summarize(result):
    if any('error' in row for row in result['clips']):raise RuntimeError('incomplete ablation run')
    metrics=[r['metrics'] for r in result['clips']]
    wall=sum(m['wall_seconds'] for m in metrics)
    times=[t for m in metrics for t in m['frame_latency_ms']]
    rows=[]
    for row in result['clips']:
        root=Path('data/evaluation')/result['run_id']/row['clip']['id']
        samples=[json.loads(line) for line in (root/'diagnostics.jsonl').read_text().splitlines()]
        counts=Counter(t['track_id'] for s in samples for t in s['tracks'])
        m=row['metrics']
        rows.append({'id':row['clip']['id'],'sha256':row['clip']['sha256'],
            'label':row['clip']['event_present'],'candidate_times':m['candidate_times'],
            'dismissed_candidates':m['dismissed_candidates'],'review_times':m['human_review_times'],
            'latency_seconds':row['latency_seconds'],'ids':m['distinct_track_ids'],
            'dominant_track_frames':max(counts.values(),default=0),'sampled_frames':len(samples),
            'no_detection_frames':sum(not s['detections'] for s in samples),'fps':m['processing_fps'],
            'p50_ms':m['p50_ms'],'p95_ms':m['p95_ms'],'root':str(root).replace('\\','/')})
    c=result['comparison']['temporal']
    return {'run_id':result['run_id'],'configuration':result['configuration'],
        'recall':c['event_recall'],'true_positive_clips':c['true_positive_clips'],
        'false_positive_clip_rate':c['false_positive_clip_rate'],
        'false_positive_clips':c['false_positive_clips'],'false_candidates':c['false_alert_events'],
        'dismissed_candidates':sum(m['dismissed_candidates'] for m in metrics),
        'review_events':sum(len(m['human_review_times']) for m in metrics),
        'fps':sum(m['sampled_frames'] for m in metrics)/wall,
        'p50_ms':float(np.percentile(times,50)),'p95_ms':float(np.percentile(times,95)),
        'cpu_one_core_percent':sum(m['cpu_one_core_percent']*m['wall_seconds'] for m in metrics)/wall,
        'memory_measurements':[m['memory'] for m in metrics],'clips':rows}


def main():
    root=Path('evaluation/phase1b')
    results={v:json.loads((root/v/'results.json').read_text()) for v in 'ABCDE' if (root/v/'results.json').exists()}
    if not all(v in results for v in 'ABCD'):raise RuntimeError('A-D must finish first')
    reference=[(r['clip']['id'],r['clip']['sha256'],r['clip']['event_present']) for r in results['A']['clips']]
    for v,r in results.items():
        assert [(x['clip']['id'],x['clip']['sha256'],x['clip']['event_present']) for x in r['clips']]==reference
    # Verify that tracking/temporal ablations consumed identical real detections.
    for i in range(len(reference)):
        inputs=[]
        for v in 'ABCD':
            r=results[v];p=Path('data/evaluation')/r['run_id']/reference[i][0]/'diagnostics.jsonl'
            inputs.append([json.loads(s)['detections'] for s in p.read_text().splitlines()])
        assert all(value==inputs[0] for value in inputs[1:]),'detector inputs changed in A-D'
    data={v:summarize(r) for v,r in results.items()}
    (root/'ablation.json').write_text(json.dumps(data,indent=2))
    labels={'A':'Original baseline','B':'Tracking only','C':'Temporal only','D':'Tracking + temporal','E':'Initial D + low-confidence continuation (rejected)'}
    lines=['# Phase 1B held-out regression evaluation — 2026-10-27','',
        'The exact five original clips, labels and hashes are unchanged. These subjects were held out initially,',
        'but their failures now informed engineering changes. These are regression results, not unseen-test accuracy.',
        'Original results are preserved in `evaluation/phase1b/original-results.json`; A is a fresh instrumented baseline.',
        'All runs use actual OpenCV 5 YOLOX CPU inference at 640 input and 5 sampled frames/video-second.',
        'A–D consumed identical sampled detections (asserted from every diagnostic record).','',
        '## Controlled ablation','',
        '| Variant | Fall recall | Non-fall FP clips | False candidates | Final dismissed | Review events | FPS | p50 / p95 ms | CPU % of one core |',
        '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for v,s in data.items():
        lines.append(f"| {v}: {labels[v]} | {s['true_positive_clips']}/2 ({s['recall']:.0%}) | {s['false_positive_clips']}/3 ({s['false_positive_clip_rate']:.1%}) | {s['false_candidates']} | {s['dismissed_candidates']} | {s['review_events']} | {s['fps']:.2f} | {s['p50_ms']:.1f} / {s['p95_ms']:.1f} | {s['cpu_one_core_percent']:.1f} |")
    lines += ['', 'FPS is total processed frames / total replay wall time. Percentiles pool measured per-frame latencies.',
        'Inference, motion, evidence/debug encoding and diagnostic I/O are included. Model setup is excluded from replay time.',
        'Runs were sequential, not repeated/randomized; CPU scheduling/thermal variation prevents causal speedup claims.',
        'No configuration sustains the requested live 5 FPS. Memory API measurements are retained in ablation.json;',
        'Windows peak memory is process-lifetime, not an independent per-clip peak.','', '## Per-clip results','',
        '| Variant / clip | Candidate times (s) | Onset latency (s) | Dismissed | IDs | Dominant ID frames / sampled | No detection frames | FPS | p50 / p95 ms |',
        '|---|---|---:|---:|---:|---:|---:|---:|---:|']
    for v,s in data.items():
        for r in s['clips']:
            stamps=', '.join(f'{t:.3f}' for t in r['candidate_times']) or 'none'
            latency=f"{r['latency_seconds']:.3f}" if r['latency_seconds'] is not None else '—'
            lines.append(f"| {v} / {r['id']} | {stamps} | {latency} | {r['dismissed_candidates']} | {r['ids']} | {r['dominant_track_frames']}/{r['sampled_frames']} | {r['no_detection_frames']} | {r['fps']:.2f} | {r['p50_ms']:.1f} / {r['p95_ms']:.1f} |")
    lines += ['', 'Dominant-ID coverage and distinct-ID counts are continuity proxies, not ground-truth IDF1/HOTA.',
        'Extra detections may be false people or duplicate boxes. They must not be interpreted as true person counts.',
        'Onset latency uses the unchanged publisher labels and video time, not wall-clock notification latency.',
        'A dismissed false candidate still counts as a false candidate. Fall candidates and human-review events are separate.',
        '', '## Development regression cross-check','',
        'A full initial combined run on the original development set detected 10/11 falls but introduced two false candidates',
        'among 13 negatives: clip_06 (squat) and gmdcsa_ADL_13 (compact sitting). Both came from the optional compact-low branch,',
        'without horizontal posture. That branch was removed; horizontal geometry remains necessary but is insufficient alone.',
        'Replaying all 25 clips\' recorded real detections and motion through the final temporal estimator gives 10/11 falls and 0/13 FP clips.',
        'This is a temporal-only recorded-evidence regression, not a second full detector benchmark; it has no FPS claim.',
        'The original initial run is in evaluation/phase1b/development/results.json; final replay provenance and hashes are in',
        'evaluation/phase1b/development-final-replay.json. Both negative clips also have full-inference integration tests.',
        '', '## Diagnosis and changes','',
        'Subject 2 Fall/13: track 1 reaches RAPID_DESCENT at 3.211 s. No detections occur at 3.412 and 3.612 s.',
        'The next horizontal detection at 3.813 s receives a new ID: the 0.602 s observation gap exceeds the old 0.5 s expiry.',
        'Subject 3 Fall/16: last upright track-1 observation is at 1.804 s; five intervening sampled frames have no detections.',
        'The next horizontal person at 3.007 s receives a new ID after a 1.203 s gap. The fall transition is not directly observed.',
        'Thus detector coverage, track expiry and temporal reset interact. Sampling is still 5 FPS; these are missing detections',
        'at sampled instants, not skipped timeline rows. Denser inference has not been shown to recover the transition.',
        'Candidate scoring and dismissal do not explain the false negatives: no candidate reached either stage.',
        '', 'B retains unmatched track identities for up to 1.5 s, caps velocity prediction at 0.25 s, gates area changes,',
        'and rejects ambiguous gap reattachment. It emits only actual detections. It does not fabricate/interpolate boxes.',
        'B alone cannot overcome the original temporal reset. C alone cannot recover history across changed track IDs.',
        'D combines retention with a bounded sequence rule: an observed upright reference, net downward center displacement',
        '(at least 0.18 reference heights), average downward speed (at least 0.15 heights/s), height loss and horizontal geometry.',
        'The window remains 1.5 s; observed endpoints may support a candidate when intermediate states are unavailable.',
        'This is explicitly weaker evidence than observing the entire descent, and does not prove a fall during occlusion.',
        'Missing or low-confidence observations reset stationarity. Recovery requires observed upward movement and upright geometry.',
        '', 'Subject 3 ADL/09 is getting up from the floor, including a crouched/bent pose. At 5.430 s box jitter gives a downward',
        'velocity spike (~62.9 px/s); at 6.435 s the box becomes wide, although its center is moving upward (~−6.1 px/s).',
        'The old recent-descent latch combines these unrelated cues into a candidate, dismissed at 6.837 s.',
        'The new net-displacement rule rejects that sequence. No filename, subject, onset or label enters the perception modules.',
        '', 'E, when present, lowers the detection score floor to 0.15 only for association to existing tracks;',
        'new identities still require 0.30. High-confidence matches are assigned first. Low-confidence boxes cannot establish immobility.',
        'E uses the initial temporal variant, before the development-squat correction. It is a detector exploration, not the selected default.',
        'Its earlier Subject 3 alert uses a confidence-0.276 box roughly 482x203 pixels wide over much of the room.',
        'More raw detections therefore do not establish better localization; the earlier latency is not trusted evidence of an earlier observed fall.',
        'The final temporal rule removes the initial compact-low branch after a development squat triggered it.',
        'Horizontal geometry alone is still insufficient: net descent, speed, height loss and bounded upright history are also required.','',
        '## Evidence artifacts','',
        'Each run includes diagnostics.jsonl, timeline.csv, state-transitions.json, final-decision.json, original/annotated frames,',
        'trajectory overlays and a real debug.avi. Timelines include dimensions, center, area, displacement, velocity, flow, state and reasons.','']
    for v in ['A','D']:
        for r in data[v]['clips']:
            base='../../'+r['root']
            lines.append(f"- {v} {r['id']}: [timeline]({base}/timeline.csv), [frames]({base}/contact.jpg), [video]({base}/debug.avi), [transitions]({base}/state-transitions.json), [decision]({base}/final-decision.json).")
    lines += ['', '## Known failures and gate','',
        'The small reused set cannot establish generalization. Detection misses, duplicate boxes, occlusion ambiguity,',
        'seated/foreshortened falls, real multi-person crossings, camera motion, natural fall/recovery and physical-camera tests remain unresolved.',
        'Long gaps are intentionally not bridged; identity preservation is not proof that an unobserved motion was a fall.',
        '**INCOMPLETE — perception still needs work.** Do not begin Phase 2.',
        'Highest-priority next fix: improve real person-detection coverage during descent/prone poses, then evaluate on fresh untouched subjects.',
        'See docs/phase-1-report.md for the test outcome and selected operating configuration.']
    Path('evaluation/holdout/report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    Path('evaluation/holdout/results.json').write_text(json.dumps({**results['D'],
        'scope':'Phase 1B regression ablation, not unseen generalization','selected_variant':'D','variants':data},indent=2))


if __name__=='__main__':main()
