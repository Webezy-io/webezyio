# typescript

This project has been generated thanks to [```Webezy.io```](https://www.webezy.io) !

This project is using gRPC as main code generator and utilize HTTP2 + protobuf protocols for communication.

# CLI steps
This project has been generated thanks to webezy.io CLI using the following steps:

```sh
(wz-venv) amitshmulevitch@Amits-MacBook-Pro samples % wz n typescript
[*] Creating new webezy project "typescript"
[?] Choose server language: Typescript
   Python
 ❯ Typescript

[?] Choose clients languages (Use arrows keys to enable disable a language): 
   ◯ Python
 ❯ ◉ Typescript

[?] Enter domain name: webezy
[?] Enter a root dir path: /Users/amitshmulevitch/Projects/wz/webezyio/samples/typescript
[*] Server language: typescript
[*] Adding client: typescript
[*] Success !
	Created new project "typescript"
	-> cd /Users/amitshmulevitch/Projects/wz/webezyio/samples/typescript
	-> And then continue developing your awesome services !
-> For more info on how to use the webezy.io CLI go to https://www.webezy.io/docs
(wz-venv) amitshmulevitch@Amits-MacBook-Pro samples % cd typescript 
(wz-venv) amitshmulevitch@Amits-MacBook-Pro typescript % wz g p
[*] Generating new resource 'package'
[?] Enter package name: SamplePackage
[*] Success !
	Created new package "SamplePackage"
(wz-venv) amitshmulevitch@Amits-MacBook-Pro typescript % wz -e g s
[*] Creating resource in expanded mode
[*] Generating new resource 'service'
[?] Enter service name: SampleService
[?] Choose service dependencies: 
 ❯ ◉ domain.SamplePackage.v1

[*] Success !
	Created new service "SampleService"
(wz-venv) amitshmulevitch@Amits-MacBook-Pro typescript % wz g m
[*] Generating new resource 'message'
[?] Enter message name: SampleMessage
[?] Choose a package to attach the message: SamplePackage [domain.SamplePackage.v1]
 ❯ SamplePackage [domain.SamplePackage.v1]

[?] Enter field name: SampleString
[?] Choose field type: string
   double
   float
   int64
   int32
   bool
 ❯ string
   message
   bytes
   enum

[?] Choose field label: optional
 ❯ optional
   repeated

[?] Add more fields? (Y/n): n

[*] Created Message !

(wz-venv) amitshmulevitch@Amits-MacBook-Pro typescript % wz g r
[*] Generating new resource 'rpc'
[?] Enter rpc name: SampleUnary
[?] Choose a service to attach the rpc: SampleService
 ❯ SampleService

[?] Choose message type: Unary
 ❯ Unary
   Client stream
   Server stream
   Bidi stream

[?] Choose the input type: domain.SamplePackage.v1.SampleMessage
 > domain.SamplePackage.v1.SampleMessage

[?] Choose the output type: domain.SamplePackage.v1.SampleMessage
 > domain.SamplePackage.v1.SampleMessage

```

# Index
Usage:
- [Typescript](#Typescript)

Resources:
- [SampleService](#SampleService)
- [SamplePackage](#domain.SamplePackage.v1)

# Services

## SampleService

__SampleUnary__ [Unary]
- Input: [domain.SamplePackage.v1.SampleMessage](#SampleMessage)
- Output: [domain.SamplePackage.v1.SampleMessage](#SampleMessage)

# Packages

## domain.SamplePackage.v1

### SampleMessage

__SampleString__ [TYPE_STRING]



# Usage
This project supports clients communication in the following languages:
### Typescript

```ts
import { typescript } from './clients/typescript/';

let client = new typescript();

// Unary call
client.<Unary>(<InMessage>)
	.then((res:<OutMessage>) => {
		console.log(res);
	}).catch((err: any) => console.log(err));

// Server Stream
client.<ServerStream>(<InMessage>)
	.subscribe((res: <OutMessage>) => {
		console.log(res);
	})

// Client Stream

// Bidi Stream
responses = client.<BidiStream>()
	.subscribe((res: <OutMessage>) => {
		console.log(res)
	})

responses.write(<InMessage>)
```

* * *
__This project and README file has been created thanks to [webezy.io](https://www.webezy.io)__