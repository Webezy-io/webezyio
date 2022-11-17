# TEST-PROJECT

This project has been generated thanks to [```Webezy.io```](https://www.webezy.io) !

This project is using gRPC as main code generator and utilize HTTP2 + protobuf protocols for communication.

# Index
Usage:
- [Python](#Python)

Resources:
- [SampleService](#SampleService)
- [OtherPackage](#webezy.OtherPackage.v1)
- [SamplePackage](#webezy.SamplePackage.v1)

# Services

## SampleService

__SampleRPC__ [Unary]
- Input: [webezy.SamplePackage.v1.SampleMessage](#SampleMessage)
- Output: [webezy.SamplePackage.v1.SampleMessage](#SampleMessage)

__TestRPC__ [Client stream]
- Input: [webezy.OtherPackage.v1.OtherMessage](#OtherMessage)
- Output: [webezy.OtherPackage.v1.OtherMessage](#OtherMessage)

__OtherRPC__ [Client stream]
- Input: [webezy.OtherPackage.v1.OtherMessage](#OtherMessage)
- Output: [webezy.SamplePackage.v1.SampleMessage](#SampleMessage)

# Packages

## webezy.OtherPackage.v1

### OtherMessage

__StringField__ [TYPE_STRING]



## webezy.SamplePackage.v1

### SampleMessage

__ExtendedField__ [TYPE_BOOL]


__Timestamp__ [[Timestamp](#Timestamp)]


__Integer__ [TYPE_INT32]


__ChildMessage__ [[OtherMessage](#OtherMessage)]


__test__ [TYPE_MAP]


__testNestedMap__ [TYPE_MAP]


__testEnumMap__ [TYPE_MAP]



### ExtensionMessage

__BoolExtend__ [TYPE_BOOL]


__TestString__ [TYPE_STRING]



# Usage
This project supports clients communication in the following languages:
### Python

```py
from clients.python import testproject

client = testproject()

# Unary call
response = stub.<Unary>(<InMessage>())
print(response)

# Server stream
responses = stub.<ServerStream>(<InMessage>())
for res in responses:
	print(res)

# Client Stream
requests = iter([<InMessage>(),<InMessage>()])
response = client.<ClientStream>(requests)
print(response)

# Bidi Stream
responses = client.<BidiStream>(requests)
for res in responses:
	print(res)
```


* * *
__This project and README file has been created thanks to [webezy.io](https://www.webezy.io)__