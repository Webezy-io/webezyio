from webezyio import _resources
module = _resources.parse_proto('test.proto')
print(dir())
pool = _resources.parse_pool(module.pool)
msg = _resources.find_message('Test',pool)
print(msg.GetOptions())

