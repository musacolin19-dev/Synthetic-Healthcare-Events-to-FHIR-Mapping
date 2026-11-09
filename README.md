# Synthetic Healthcare Events to FHIR Mapping

A small healthcare interoperability ETL that validates synthetic patient encounter data and maps it into simplified FHIR R4 Encounter resources. Uses generated patient references rather than identifiable data, validates timestamps and statuses, and quarantines malformed records. An educational demo of health data normalization, not a compliance-certified system.

## Quick start

```bash
python fhir_etl.py --input samples/encounters.csv --output output
python -m unittest discover -s tests -v
```

## Architecture and scope

Source CSV → validation → FHIR-shaped JSON resources and quarantine file. Does not transmit clinical data, connect to real EHRs, or assert HIPAA compliance. Real-world use needs profile validation, terminology mappings, privacy and security controls.

**Portfolio note:** Original educational starter code, not a production deployment. Use only synthetic/public datasets, document your own extensions, and test integrations before claiming production experience.
