"""Counterfactual temporal regression on recorded real detections/motion, not an FPS benchmark."""
import argparse
import hashlib
import json
from pathlib import Path
from vision.schemas import Config,Detection,Motion
from vision.tracking import Track
from vision.temporal_v2 import SequenceEstimator


def main():
    parser=argparse.ArgumentParser();parser.add_argument('results');parser.add_argument('--output',required=True)
    parser.add_argument('--set',action='append',default=[],help='Config override key=value (JSON value), counterfactual only')
    args=parser.parse_args();source=json.loads(Path(args.results).read_text())
    config=dict(source['configuration']);config.pop('minimum_ground_width_ratio',None)
    config.update(improved_tracking=True,improved_temporal=True)
    for item in args.set:
        key,value=item.split('=',1);config[key]=json.loads(value)
    rows=[]
    for row in source['clips']:
        clip=row['clip']
        assert hashlib.sha256(Path(clip['path']).read_bytes()).hexdigest()==clip['sha256']
        p=Path('data/evaluation')/source['run_id']/clip['id']/'diagnostics.jsonl'
        samples=[json.loads(s) for s in p.read_text().splitlines()]
        estimator=SequenceEstimator(Config(**config));events=[];dismissals=[]
        for sample in samples:
            estimator.prune([k for k,m in estimator.memory.items() if sample['timestamp']-m.last<=config['track_hold_seconds']])
            for tr in sample['tracks']:
                prior=tr['observation']
                o=estimator.update(Track(tr['track_id'],Detection.model_validate(prior['detection'])),
                                   Motion.model_validate(prior['motion']),prior['camera_id'])
                if o.fall_event_detected:events.append(o.timestamp)
                if o.action=='dismiss':dismissals.append(o.timestamp)
        rows.append({'id':clip['id'],'event_present':clip['event_present'],'candidate_times':events,
                     'dismissal_times':dismissals,'diagnostics_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    positive=[r for r in rows if r['event_present'] is True];negative=[r for r in rows if r['event_present'] is False]
    result={'scope':'temporal-only replay of measured real detections and motion; no new detector inference or FPS claim',
        'source_results':args.results,'source_run_id':source['run_id'],'configuration':config,
        'true_positive_clips':sum(bool(r['candidate_times']) for r in positive),'positive_clips':len(positive),
        'false_positive_clips':sum(bool(r['candidate_times']) for r in negative),'negative_clips':len(negative),'clips':rows}
    Path(args.output).write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k not in ('clips','configuration')},indent=2))


if __name__=='__main__':main()
