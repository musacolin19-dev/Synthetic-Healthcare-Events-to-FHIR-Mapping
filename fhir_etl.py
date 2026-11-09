import argparse,csv,hashlib,json
from datetime import datetime
from pathlib import Path
VALID_STATUSES={'planned','in-progress','finished','cancelled'}

def map_row(row):
    if row.get('status') not in VALID_STATUSES:raise ValueError('invalid encounter status')
    start=datetime.fromisoformat(row['start'].replace('Z','+00:00'))
    if start.tzinfo is None:raise ValueError('timestamp must have timezone')
    if not row.get('encounter_id') or not row.get('synthetic_patient_id'):raise ValueError('missing identifier')
    subject=hashlib.sha256(row['synthetic_patient_id'].encode()).hexdigest()[:16]
    return {'resourceType':'Encounter','id':row['encounter_id'], 'status':row['status'],
            'class':{'system':'http://terminology.hl7.org/CodeSystem/v3-ActCode','code':'AMB'},
            'subject':{'reference':f'Patient/{subject}'},'period':{'start':start.isoformat()}}

def transform(rows):
    good,bad=[],[]
    for row in rows:
        try:good.append(map_row(row))
        except (ValueError,KeyError,TypeError) as exc:bad.append({'row':row,'error':str(exc)})
    return good,bad

def run(src,dest):
    with Path(src).open(newline='') as f:good,bad=transform(csv.DictReader(f))
    Path(dest).mkdir(parents=True,exist_ok=True)
    (Path(dest)/'encounters.fhir.json').write_text(json.dumps({'resourceType':'Bundle','type':'collection','entry':[{'resource':x} for x in good]},indent=2))
    (Path(dest)/'quarantine.json').write_text(json.dumps(bad,indent=2))
    return {'valid':len(good),'quarantined':len(bad)}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',default='output');a=p.parse_args();print(run(a.input,a.output))
