/* eslint-disable */
import _m0 from "protobufjs/minimal";

/** Webezy.io Generated proto DO NOT EDIT */

/** [webezyio] - None */
export interface SampleMessage {
  /** [webezyio] - */
  SampleString: string;
}

function createBaseSampleMessage(): SampleMessage {
  return { SampleString: "" };
}

export const SampleMessage = {
  encode(message: SampleMessage, writer: _m0.Writer = _m0.Writer.create()): _m0.Writer {
    if (message.SampleString !== "") {
      writer.uint32(10).string(message.SampleString);
    }
    return writer;
  },

  decode(input: _m0.Reader | Uint8Array, length?: number): SampleMessage {
    const reader = input instanceof _m0.Reader ? input : new _m0.Reader(input);
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

  fromJSON(object: any): SampleMessage {
    return { SampleString: isSet(object.SampleString) ? String(object.SampleString) : "" };
  },

  toJSON(message: SampleMessage): unknown {
    const obj: any = {};
    message.SampleString !== undefined && (obj.SampleString = message.SampleString);
    return obj;
  },

  fromPartial<I extends Exact<DeepPartial<SampleMessage>, I>>(object: I): SampleMessage {
    const message = createBaseSampleMessage();
    message.SampleString = object.SampleString ?? "";
    return message;
  },
};

type Builtin = Date | Function | Uint8Array | string | number | boolean | undefined;

type DeepPartial<T> = T extends Builtin ? T
  : T extends Array<infer U> ? Array<DeepPartial<U>> : T extends ReadonlyArray<infer U> ? ReadonlyArray<DeepPartial<U>>
  : T extends {} ? { [K in keyof T]?: DeepPartial<T[K]> }
  : Partial<T>;

type KeysOfUnion<T> = T extends T ? keyof T : never;
type Exact<P, I extends P> = P extends Builtin ? P
  : P & { [K in keyof P]: Exact<P[K], I[K]> } & { [K in Exclude<keyof I, KeysOfUnion<P>>]: never };

function isSet(value: any): boolean {
  return value !== null && value !== undefined;
}
