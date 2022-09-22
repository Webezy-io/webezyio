import _m0 from "protobufjs/minimal";
export interface SampleMessage {
    SampleString: string;
}
export declare const SampleMessage: {
    encode(message: SampleMessage, writer?: _m0.Writer): _m0.Writer;
    decode(input: _m0.Reader | Uint8Array, length?: number): SampleMessage;
    fromJSON(object: any): SampleMessage;
    toJSON(message: SampleMessage): unknown;
    fromPartial<I extends {
        SampleString?: string | undefined;
    } & {
        SampleString?: string | undefined;
    } & { [K in Exclude<keyof I, "SampleString">]: never; }>(object: I): SampleMessage;
};
