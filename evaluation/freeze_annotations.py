"""Transcribe blind visual annotations; never reads detector predictions."""
import hashlib
import json
from pathlib import Path

# Visible body, main camera view only for ASSIST composites. Preview xyxy pixels.
BOXES = {
'fresh_gmd4_Fall_03': [[14,0,174,240],[39,0,173,240],[46,85,175,240],[40,158,160,240],[26,177,156,240],[25,178,163,240]],
'fresh_gmd4_Fall_07': [[82,44,188,166],[96,68,188,165],[85,99,184,168],[50,119,187,166],[57,117,189,167],[58,119,188,167]],
'fresh_gmd4_Fall_08': [[48,42,122,151],[49,45,132,151],[47,65,151,150],[47,87,155,154],[47,87,155,154],[47,87,155,154]],
'fresh_gmd4_Fall_11': [[119,0,160,161],[96,0,162,162],[48,70,159,163],[49,128,160,164],[49,128,160,164],[49,128,160,164]],
'fresh_gmd4_ADL_14': [[69,3,135,165],[61,7,110,156],[40,28,119,157],[78,0,120,164],[70,0,122,165],[78,0,122,162]],
'fresh_gmd4_ADL_17': [[],[55,0,111,161],[80,59,152,159],[78,17,130,161],[51,6,90,158],[32,11,63,156]],
'fresh_assist_02_fall_backward': [[145,15,178,95],[140,83,243,119],[140,83,244,120],[140,83,244,120],[140,83,244,120],[145,31,180,94]],
'fresh_assist_04_forward_fall_jogging': [[17,26,36,89],[47,56,106,115],[46,90,128,135],[46,91,128,135],[46,91,128,135],[46,91,128,135]],
'fresh_assist_05_vertical_fall_faint': [[40,0,82,102],[55,33,110,111],[54,88,145,138],[54,88,145,138],[54,88,145,138],[54,88,145,138]],
'fresh_assist_07_fall_to_knees_forward': [[46,0,99,110],[48,32,145,134],[52,98,164,160],[52,98,164,160],[52,98,164,160],[52,98,164,160]],
'fresh_assist_01_walking_slowly': [[162,24,213,161],[145,29,185,141],[102,31,127,102],[76,34,98,91],[57,34,78,86],[47,34,63,83]],
'fresh_assist_12_sitting_laying_down_quickly': [[144,42,183,96],[144,46,182,96],[146,80,198,108],[146,63,189,99],[146,43,183,97],[146,43,183,97]],
'fresh_assist_13_bending_at_knees': [[39,26,61,86],[33,49,59,86],[33,61,58,86],[33,61,57,86],[40,27,61,86],[39,27,61,86]],
'fresh_assist_14_bending_wo_knees': [[43,26,67,86],[43,26,67,86],[40,53,67,87],[40,53,67,87],[40,53,67,87],[45,27,68,87]],
}
PHASES = {
'fresh_gmd4_Fall_03':['upright','upright','descent','ground','ground','ground'],
'fresh_gmd4_Fall_07':['descent','descent','descent','ground','ground','ground'],
'fresh_gmd4_Fall_08':['seated','descent','descent','ground','ground','ground'],
'fresh_gmd4_Fall_11':['upright','descent','descent','ground','ground','ground'],
'fresh_assist_02_fall_backward':['upright','ground','ground','ground','ground','recovery'],
'fresh_assist_04_forward_fall_jogging':['upright','descent','ground','ground','ground','ground'],
'fresh_assist_05_vertical_fall_faint':['upright','descent','ground','ground','ground','ground'],
'fresh_assist_07_fall_to_knees_forward':['upright','descent','ground','ground','ground','ground'],
}

def main():
    target=Path('datasets/phase1c/annotations.json')
    if target.exists(): raise FileExistsError('annotations already frozen')
    index=json.loads(Path('data/phase1c-annotation/index.json').read_text())
    for clip in index:
        key=clip['clip_id']
        clip['main_view_preview_roi'] = ([108,0,320,180] if ('02_fall_backward' in key or '12_sitting' in key) else [0,0,213,180]) if 'assist' in key else [0,0,320,240]
        for n,frame in enumerate(clip['frames']):
            frame['box_preview_xyxy']=BOXES[key][n]
            frame['phase']=PHASES.get(key,['nonfall']*6)[n]
            frame['reference_identity']=1
    result={'method':'Single AI visual annotator, raw images before model inference; visible-body boxes, approximate +/-6 preview pixels; sparse exploratory audit, not expert or full-frame ground truth. ASSIST inset excluded from localization scoring, retained in pipeline input. Same person in two views is not multi-person evidence.', 'clips':index}
    target.write_text(json.dumps(result,indent=2))
    Path('datasets/phase1c/annotations.sha256').write_text(hashlib.sha256(target.read_bytes()).hexdigest()+'\n')

if __name__=='__main__': main()
