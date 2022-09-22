"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const grpc_js_1 = require("@grpc/grpc-js");
const SampleService_1 = require("./services/SampleService");
let _PORT = 50051;
let _HOST = '0.0.0.0';
let _ADDR = `${_HOST}:${_PORT}`;
const server = new grpc_js_1.Server({
    "grpc.max_receive_message_length": -1,
    "grpc.max_send_message_length": -1,
});
server.addService(SampleService_1.SampleServiceService, new SampleService_1.SampleService());
server.bindAsync(_ADDR, grpc_js_1.ServerCredentials.createInsecure(), (err, bindPort) => {
    if (err) {
        throw err;
    }
    console.log(`[webezy] Starting gRPC:server:${bindPort}`, `at -> ${new Date().toLocaleString()})`);
    server.start();
});
//# sourceMappingURL=server.js.map