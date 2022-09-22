/// <reference types="node" />
import { CallOptions, ChannelCredentials, ChannelOptions, Client, ClientUnaryCall, handleUnaryCall, Metadata, ServiceError, UntypedServiceImplementation } from "@grpc/grpc-js";
import { SampleMessage } from "./SamplePackage";
export declare type SampleServiceService = typeof SampleServiceService;
export declare const SampleServiceService: {
    readonly sampleUnary: {
        readonly path: "/SampleService/SampleUnary";
        readonly requestStream: false;
        readonly responseStream: false;
        readonly requestSerialize: (value: SampleMessage) => Buffer;
        readonly requestDeserialize: (value: Buffer) => SampleMessage;
        readonly responseSerialize: (value: SampleMessage) => Buffer;
        readonly responseDeserialize: (value: Buffer) => SampleMessage;
    };
};
export interface SampleServiceServer extends UntypedServiceImplementation {
    sampleUnary: handleUnaryCall<SampleMessage, SampleMessage>;
}
export interface SampleServiceClient extends Client {
    sampleUnary(request: SampleMessage, callback: (error: ServiceError | null, response: SampleMessage) => void): ClientUnaryCall;
    sampleUnary(request: SampleMessage, metadata: Metadata, callback: (error: ServiceError | null, response: SampleMessage) => void): ClientUnaryCall;
    sampleUnary(request: SampleMessage, metadata: Metadata, options: Partial<CallOptions>, callback: (error: ServiceError | null, response: SampleMessage) => void): ClientUnaryCall;
}
export declare const SampleServiceClient: {
    new (address: string, credentials: ChannelCredentials, options?: Partial<ChannelOptions> | undefined): SampleServiceClient;
    service: typeof SampleServiceService;
};
