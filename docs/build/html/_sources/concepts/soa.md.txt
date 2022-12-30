# Service Oriented Architecture

Service-oriented architecture (SOA) is a software design pattern that organizes a system as a collection of interconnected services. SOA is designed to allow different services to communicate with each other through a well-defined interface.

The main idea behind SOA is to build a system by connecting independent services, rather than building a monolithic application. This allows each service to focus on a specific task, and to be developed and maintained independently of the other services in the system.

SOA systems are typically built using a distributed architecture, where different services are deployed on separate servers or machines. This allows for flexibility and scalability, as services can be added or removed without affecting the entire system.

SOA has many benefits, including:

- Modularity: Services can be developed and maintained independently of each other, which makes it easier to update and improve the system.

- Reusability: Services can be reused in multiple applications, which can reduce development time and cost.

- Interoperability: Services can communicate with each other using a well-defined interface, which allows for integration with other systems and technologies.

- Scalability: Services can be added or removed without affecting the entire system, which makes it easier to scale the system up or down as needed.

Overall, SOA is a powerful software design pattern that can help organizations build flexible and scalable systems that are easy to maintain and improve over time.

## How Webezy.io Serving SOA

Webezy.io is utulizing `gRPC` which is framework for `RPC` - the very concept of Remote Procedure Call is to implement a distributed system
with abstract layer of communication, so when you call a native function on some place it will call a process execution on other remote computers.

`gRPC` doing that transperent communication with `HTTP2` and `Protobuf`

The `HTTP2` doing all the communication layer and `Protobuf` handling the serilization / deserialization from one code module to the other - in other words for example it's a data manipulation layer to marshel and unmarshel object from `Python` call to the remote server in `Typescript` and vice versa.

`gRPC` let you define your "Services" and thier respectively "Methods" (RPC's) in a generic way with `Protobuf` (IDL) which later compiles to native modules in the required language which makes the communication handling and the object modules.

Each RPC should know which Object it will get and which it will respond with, this "Objects" can be refrenced as "JSON" in a `HTTP1 Over JSON` system as the JSON themselvs, but we will call them in thier right name simple as "Messages" - they are not JSON ! they are `Protobuf` Objects which is much more effiecient from JSON - About 30% avg. less memory.

`Webezy.io` wrapping the `gRPC` functionality with a simple to use CLI that handling the project creation process (Project Structuring, Auto-generated Code, Correct Workflows Enforcments and more).

It follows the well-defined concepts of `gRPC` and Service Oriented Architecture in a way of each project has a well-defined "Resources" that can be described in short with the two main resources:

- Packages - A centralized module for all domain-specific "Messages" (Objects)

- Services - A service which holds 1 or more RPC, a service most import atleast 1 package to use it's "Messages" as I/O on the RPC's it implements

> __Note__ To create a resource with `Webezy.io` CLI just write
```sh
webezy generate package # Generate new package
webezy generate service # Generate new service
```

When you define those resources `Webezy.io` build the resources into `Protobuf` Files and compile them into the native implementations by the project configurations.