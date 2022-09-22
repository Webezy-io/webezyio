"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.SampleServiceService = exports.SampleService = void 0;
const grpc_js_1 = require("@grpc/grpc-js");
const error_1 = require("./utils/error");
const SampleService_1 = require("./protos/SampleService");
Object.defineProperty(exports, "SampleServiceService", { enumerable: true, get: function () { return SampleService_1.SampleServiceService; } });
class SampleService {
    constructor() {
        this.sampleUnary = (call, callback) => {
            callback(new error_1.ServiceError(grpc_js_1.status.UNIMPLEMENTED, "Method is not yet implemented"));
        };
    }
}
exports.SampleService = SampleService;
//# sourceMappingURL=SampleService.js.map