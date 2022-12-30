# Well Known Types

`Protobuf` introduced a set of "well-known" message types taht can be imported in any `.proto` file, those messages can save you to configure some already well structured messages that can become in handy.

Some of the supported "Well-knowns" in `webezy.io` projects:

- `google.protobuf.Timestamp`
- `google.protobuf.Struct`
- `google.protobuf.Value`

To be supported:

- `google.protobuf.Any`

## Import "Well-Known" Package Into `Webezy.io` Project Resource

`Webezy.io` CLI provide easy way to import packages into your `Services` and `Packages`, Use the CLI command `wz package <need.to.import> <target>`.

The convention names are as follow consider we have a package by the full name : `domain.package.v1` we then want to use the prebuilt message `Timestamp` we need first to import it's package to where we want tu use it (`domain.package.v1`) by running the following command:

```sh
$ wz package google.protobuf.Timestamp domain.package.v1

[*] Attaching package 'google.protobuf.Timestamp' -> 'domain.package.v1' package
```

In the same way if we want later to import our `domain.package.v1` package messages to be used in our new service we just created by the name `service` we need to run the following command:

```sh
wz package domain.package.v1 service

[*] Attaching package 'domain.package.v1' -> 'service' service
```

## Use "Well-Known" Type

Then we can use the new messages available under `google.protobuf.Timestamp` package(in this case only one message available by the name `Timestamp`), as nested field type -> `TYPE_MESSAGE`.

```sh
$ wz g m

[*] Generating new resource 'message'
[?] Enter message name: test
[?] Choose a package to attach the message: package [domain.package.v1]
 ❯ package [domain.package.v1]

[?] Enter field name: timestamp
[?] Choose field type: message
   double
   float
   int64
   int32
   bool
   string
 ❯ message
   bytes
   enum
   oneof
   map

[?] Choose field label: optional
 ❯ optional
   repeated

[?] Choose available messages: Timestamp
 ❯ Timestamp

[?] Add more fields? (Y/n): n

[*] Created Message !
```

It will generate the following `proto` definition:

```proto
syntax = "proto3";

import "google/protobuf/timestamp.proto";

package domain.package.v1;

message test {
    google.protobuf.Timestamp timestamp = 1;
}
```