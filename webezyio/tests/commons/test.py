from webezyio import _helpers, _fs

# file = _fs.rFile("/Users/amitshmulevitch/Projects/wz/webezyio/webezyio/tests/builder/webezy.json",json=True)
# json = _helpers.WZJson(file)
# print(json.services)

_helpers.parse_code_file(_fs.rFile('/Users/amitshmulevitch/Projects/wz/webezyio/webezyio/tests/architect/services/SampleService.py'))