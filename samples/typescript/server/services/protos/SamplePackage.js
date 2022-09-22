"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.SampleMessage = void 0;
const minimal_1 = __importDefault(require("protobufjs/minimal"));
function createBaseSampleMessage() {
    return { SampleString: "" };
}
exports.SampleMessage = {
    encode(message, writer = minimal_1.default.Writer.create()) {
        if (message.SampleString !== "") {
            writer.uint32(10).string(message.SampleString);
        }
        return writer;
    },
    decode(input, length) {
        const reader = input instanceof minimal_1.default.Reader ? input : new minimal_1.default.Reader(input);
        let end = length === undefined ? reader.len : reader.pos + length;
        const message = createBaseSampleMessage();
        while (reader.pos < end) {
            const tag = reader.uint32();
            switch (tag >>> 3) {
                case 1:
                    message.SampleString = reader.string();
                    break;
                default:
                    reader.skipType(tag & 7);
                    break;
            }
        }
        return message;
    },
    fromJSON(object) {
        return { SampleString: isSet(object.SampleString) ? String(object.SampleString) : "" };
    },
    toJSON(message) {
        const obj = {};
        message.SampleString !== undefined && (obj.SampleString = message.SampleString);
        return obj;
    },
    fromPartial(object) {
        var _a;
        const message = createBaseSampleMessage();
        message.SampleString = (_a = object.SampleString) !== null && _a !== void 0 ? _a : "";
        return message;
    },
};
function isSet(value) {
    return value !== null && value !== undefined;
}
//# sourceMappingURL=SamplePackage.js.map