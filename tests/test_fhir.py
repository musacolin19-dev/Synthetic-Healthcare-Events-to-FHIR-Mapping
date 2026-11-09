import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from fhir_etl import transform
class TestFHIR(unittest.TestCase):
    def test_valid_and_invalid(self):
        good,bad=transform([{'encounter_id':'e','synthetic_patient_id':'p','status':'finished','start':'2026-01-01T00:00:00Z'}, {'status':'broken'}])
        self.assertEqual((len(good),len(bad)),(1,1))
        self.assertEqual(good[0]['resourceType'],'Encounter')
