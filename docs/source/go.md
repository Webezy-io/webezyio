# Developing Webezy.io Projects With `Go`

## Overview

Since `webezyio` V0.1.x we support auto-generated code for `Go`.
The project can be instantiated with running `wz n <project>` command and pass a `Go` server and or client as your language for the project.

This will add one more addition step to creating a `webezyio` project - The `Go` package value should be inputed to `protobuf` descriptors so the auto-generated modules will have the right `Go` package path.

The value you should enter is a prefix for your package as it will be concatenate with your `Project Package Name`

A common `Go` package prefix is : `github.com/`

```json
{
    "project" : {
        "name": "some-project",
        "packageName": "someproject",
        "goPackage" : "github.com/org/someproject",
        "server": {
            "language": "go"
        }
    }
}
```

This will start a `go.mod` file at the root project directory with the following entry:
```
module github.com/org/someproject
```

## Project Structure

```sh
# Root dir of your project
my-project/
├─ bin/ # Some executable scripts
├─ clients/ # All clients code in multiple languages if specified
│  ├─ go/
│     ├─ /utils
│     ├─ main.go
├─ server/ # Server file
│  ├─ server.go
├─ protos/ # Proto defintions files
│  ├─ SampleService.proto
│  ├─ Samplepackage.proto
├─ service/ # Service file and protos compiled files
│  ├─ protos/
│  │  ├─ SampleService/
│  │  │  ├─ SampleService_grpc.pb.go
│  │  ├─ Samplepackage/
│  │  │  ├─ Samplepackage.pb.go
│  ├─ SampleService/ # Sevice impl.
│  │  ├─ SampleService.go
├─ .gitignore
├─ go.mod
├─ README.md
├─ webezy.json
```

## Service

### Usage
Open your service `Go` file at `./services/<your-service>.go`
and edit the impl. of your methods.

For e.x we have a service called `SampleService` and the service serves a RPC called `SampleUnary` which is unary type... we should open the `./services/SampleService/SampleService.go` file and navigate to the following `func` : 
```go
func (SampleServiceServicer *SampleService) SampleUnary(
    ctx context.Context,
    testMessage *testPackage.TestMessage
) (response *testPackage.TestMessage, err error) {
	// Add your impl. here
}
```

## Client
`webezyio` auto-generate a `Go` package for client communication with the `Server`.
The package is a wrapper module for all channels and default configurations, and holds all project services RPC's (Methods) in centralized package that can be distributed.

### Usage
Create a new `Go` file and copy the following code:
```go
package main

import (
	client "github.com/xxx/yyy/clients/go"
	somePackage "github.com/xxx/yyy/services/protos/<some-package>"
)

func main() {
	//Init the client
	c := client.Default()
	// Alternatively more advanced custom client
	// c := client.New("localhost", 50051, []grpc.DialOption{}, []grpc.CallOption{}, metadata,MD, nil)

	// Construct a message
	msg := somePackage.SomeMessage{}

	// Send unary
	res, header, trailer := c.Find(&msg)
	fmt.Printf("Got server unary response: %v", res)
	fmt.Printf("Header: %v", init)
	fmt.Printf("Trailer: %v", trail)
}
```

> __Note__ `xxx` represent the organization name on github if any it should be specified on project creating process, `yyy` is representing the project package name

## Useful resources
- [Go gRPC official docs](https://grpc.io/docs/languages/go/)
- [Go gRPC advanced topics](https://github.com/grpc/grpc-go/tree/master/Documentation)

## Known issues

> __Warning__ Make sure you have initalized and configured `Go` on your development environement properly before trying to build a `webezyio-go` project !


For e.x make sure you have `Go` path configured at `~/.bash_profiles`
```sh
export GO_PATH=~/go
export PATH=$PATH:/$GO_PATH/bin
```


Once a project is being built a `Go` package for client wrapper code is auto-generated, this package conssist of all models under project resources (Packages->messages/enums).
When a service isnt use all of the available messages or even there is a whole package that none of your services use this error will raise at the first run after `wz build` process:

```sh
# github.com/xxx/yyy/clients/go
clients/go/main.go:18:2: imported and not used: "github.com/xxx/yyy/services/protos/<some-package>"
clients/go/main.go:20:2: imported and not used: "github.com/xxx/yyy/services/protos/<some-package>"
```

- Importing by default all packages to client generated code module
: By default when generating `Go` client the `import` statment is filled with all project packages - we plan to make a fix to this behaviour so client can be run driectly without further editions.



### Fix:
There is an easy fix to this issue - 
- Open `./clients/go/main.go` file and save it (Ctrl + S)
: It should remove all unscessery packages import that the client dosnt use.