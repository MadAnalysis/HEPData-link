import json
import jsonschema


def test_schema():

    with open("analyses_schema.json") as f:
        schema = json.load(f)
    with open("analyses.json") as f:
        test = json.load(f)

    jsonschema.validate(instance=test, schema=schema)
