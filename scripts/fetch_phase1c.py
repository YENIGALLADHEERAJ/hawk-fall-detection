"""Fetch only preregistered fresh validation media; never fetch/open the final reserve."""
import hashlib
import json
import urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


def get(url,limit=40_000_000):
    with urllib.request.urlopen(url,timeout=60) as response:data=response.read(limit+1)
    if len(data)>limit:raise ValueError('download bound exceeded')
    return data


def main():
    root=Path('datasets/phase1c');root.mkdir(exist_ok=True)
    commit=json.loads(get('https://api.github.com/repos/ASSIST-IoT-SRIPAS/multimodal-fall-detection-dataset/commits/main',1_000_000))['sha']
    entries=[]
    gmd=[('Fall','03',1.7,'forward fall'),('Fall','07',2.4,'sideways fall'),
         ('Fall','08',2.3,'backward seated fall'),('Fall','11',1.2,'forward partially visible fall'),
         ('ADL','14',None,'standing up and bending'),('ADL','17',None,'walking and picking object from floor')]
    for group,num,onset,category in gmd:
        entries.append({'id':f'fresh_gmd4_{group}_{num}',
            'source':f'https://raw.githubusercontent.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/v2.1/Subject%204/{group}/{num}.mp4',
            'event_present':group=='Fall','incident_onset':onset,'scenario':category,'dataset':'GMDCSA24',
            'subject_group':'GMDCSA24_Subject4','license':'MIT'})
    assist=[('fall','02_fall_backward'),('fall','04_forward_fall_jogging'),
            ('fall','05_vertical_fall_faint'),('fall','07_fall_to_knees_forward'),
            ('adl','01_walking_slowly'),('adl','12_sitting_laying_down_quickly'),
            ('adl','13_bending_at_knees'),('adl','14_bending_wo_knees')]
    for group,name in assist:
        entries.append({'id':'fresh_assist_'+name,
            'source':f'https://raw.githubusercontent.com/ASSIST-IoT-SRIPAS/multimodal-fall-detection-dataset/{commit}/videos/{group}/{name}.mp4',
            'event_present':group=='fall','incident_onset':None,'scenario':name,'dataset':'ASSIST-IoT reference videos',
            'subject_group':'reference demonstrators; identity not inferred','license':'CC-BY-4.0'})
    # Select final reserve by metadata only, disjoint from all viewed subjects/scenes.
    index=json.loads(Path('data/sources/zip-index.json').read_text());reserve=[]
    for group in ['Fall','ADL']:
        used=set()
        for entry in sorted(index,key=lambda v:v['name']):
            name=entry['name']
            if f'/{group}/SBJ_04_LOC2/' not in name or not name.endswith('.mp4'):continue
            activity=name.split('/')[3].split('_')[0]
            if activity in used:continue
            used.add(activity)
            reserve.append({'member':name,'source':'https://ndownloader.figshare.com/files/52990358',
                'source_label':group,'size':entry['size'],'split':'final_test_reserved',
                'status':'unopened_unrun; source label not visually adjudicated','license':'CC-BY-4.0'})
            if len(used)==4:break
    (root/'final-reserve.json').write_text(json.dumps(reserve,indent=2))
    (root/'selection.json').write_text(json.dumps({'date':'2026-10-28','assist_commit':commit,
        'selection_basis':'publisher activity metadata, before inference; final reserve never opened',
        'validation':entries},indent=2))
    def fetch(entry):
        path=Path('data/clips')/(entry['id']+'.mp4');data=get(entry['source']);path.write_bytes(data)
        return {**entry,'path':str(path).replace('\\','/'),'sha256':hashlib.sha256(data).hexdigest(),
                'split':'fresh_validation','label_provenance':'publisher activity label; onset only where supplied'}
    with ThreadPoolExecutor(max_workers=3) as pool:clips=list(pool.map(fetch,entries))
    (root/'validation.json').write_text(json.dumps(clips,indent=2))
    development=json.loads(Path('datasets/manifest.json').read_text())+json.loads(Path('datasets/holdout.json').read_text())
    (root/'development.json').write_text(json.dumps(development,indent=2))
    Path('third_party/ASSIST-LICENSE').write_bytes(get(f'https://raw.githubusercontent.com/ASSIST-IoT-SRIPAS/multimodal-fall-detection-dataset/{commit}/LICENSE',100_000))
    Path('data/sources/assist-notes.md').write_bytes(get(f'https://raw.githubusercontent.com/ASSIST-IoT-SRIPAS/multimodal-fall-detection-dataset/{commit}/notes.md',100_000))
    print('Fetched',len(clips),'validation clips; reserved',len(reserve),'unopened final clips.')


if __name__=='__main__':main()
