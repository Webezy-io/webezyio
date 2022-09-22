"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.typescript = void 0;
const grpc_js_1 = require("@grpc/grpc-js");
const util_1 = require("util");
const SampleService_1 = require("./protos/SampleService");
const _DEFAULT_OPTION = {
    "grpc.keepalive_time_ms": 120000,
    "grpc.http2.min_time_between_pings_ms": 120000,
    "grpc.keepalive_timeout_ms": 20000,
    "grpc.http2.max_pings_without_data": 0,
    "grpc.keepalive_permit_without_calls": 1,
};
class typescript {
    constructor(host = "localhost", port = 50051, metadata = new grpc_js_1.Metadata()) {
        this.host = host;
        this.port = port;
        this.metadata = metadata;
        this.SampleService_client = new SampleService_1.SampleServiceClient(`${this.host}:${this.port}`, grpc_js_1.credentials.createInsecure(), _DEFAULT_OPTION);
    }
    SampleUnary(request, metadata = this.metadata, callback) {
        if (callback === undefined) {
            return (0, util_1.promisify)(this.SampleService_client.sampleUnary.bind(this.SampleService_client))(request, metadata);
        }
        else {
            return this.SampleService_client.sampleUnary(request, metadata, callback);
        }
    }
}
exports.typescript = typescript;
//# sourceMappingURL=index.js.map