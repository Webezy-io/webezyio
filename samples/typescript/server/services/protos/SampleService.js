"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.SampleServiceClient = exports.SampleServiceService = void 0;
const grpc_js_1 = require("@grpc/grpc-js");
const SamplePackage_1 = require("./SamplePackage");
exports.SampleServiceService = {
    sampleUnary: {
        path: "/SampleService/SampleUnary",
        requestStream: false,
        responseStream: false,
        requestSerialize: (value) => Buffer.from(SamplePackage_1.SampleMessage.encode(value).finish()),
        requestDeserialize: (value) => SamplePackage_1.SampleMessage.decode(value),
        responseSerialize: (value) => Buffer.from(SamplePackage_1.SampleMessage.encode(value).finish()),
        responseDeserialize: (value) => SamplePackage_1.SampleMessage.decode(value),
    },
};
exports.SampleServiceClient = (0, grpc_js_1.makeGenericClientConstructor)(exports.SampleServiceService, "SampleService");
//# sourceMappingURL=SampleService.js.map