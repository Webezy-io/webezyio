# What is `protobuf`?

Protocol buffers, also known as `protobuf`, are a data serialization format developed by Google. They are a compact and efficient way to encode structured data for communication between systems, or for storing data in a compact and efficient manner.

Protocol buffers consist of a language- and platform-neutral schema to define the structure of the data, and code generated based on the schema to easily read and write the data in a variety of programming languages. This allows systems written in different languages to exchange data efficiently, without the need for manual parsing and serialization of data.

Protocol buffers are used in a variety of applications, including for communication between microservices, for storing data in databases, and for serializing data for storage or transmission over a network. They are designed to be fast, flexible, and simple to use, making them a popular choice for many developers.

## Syntax

`Protocol Buffer` is language-neutral, platform-neutral, extensible mechanism for serializing structured data, when we define our messages that both the services and clients of our project will know of, we define it in `.proto` files as in the following e.x:

`y.proto`
```proto

syntax = "proto3";

package x.y.z;

message Test {
    string hello = 1;
}
```

Thie small definition will be compiled to the following languages as:

### `Python`
```python
import y_pb2 as y

test = y.Test(hello="World !")
print(type(test))

# Output: <class 'y_pb2.Test'>
```

### `Typescript`
```typescript
import { Test } from 'y';

let test: Test = { hello: "World !" }
```

### `Go`
```go
package main

import (
    "y"
)

var test &y.Test
test{Hello: "World !"}
```
