# Developing Webezy.io Projects With `Typescript`

## Overview

In this article we are going over the basic concepts of developing `Webezy.io` project with `Typescript` language.

## Service Side

Each `Webezy.io` project is assigned with one or more `services`.
If your "Server Language" is configured to `Typescript` - Then you should write implementation class for each `service`.
Those Implementations will hold our core business logic for each `service` and each `RPC` of that respective `service`.

__For ex':__
We got a project called "Helloworld" and the project is holding "HelloService" (`service`) which have a "GetHello" (`RPC`) method.
We first need to go to our root directory of our project and open the `./services/HelloService.ts` file which should be created at the first time you `build` the project with `wz build` command.

When our service implemantation class has been opened we can now edit the code for our "Server Side", the class will be attached to our `server` object at start-up.

> __Note__ See `./server.ts` file to check how your services classes are beeing attached to the serving server.


## Client Side