/* eslint-disable */
import {
  CallOptions,
  ChannelCredentials,
  ChannelOptions,
  Client,
  ClientUnaryCall,
  handleUnaryCall,
  makeGenericClientConstructor,
  Metadata,
  ServiceError,
  UntypedServiceImplementation,
} from "@grpc/grpc-js";
import { SampleMessage } from "./SamplePackage";

/** Webezy.io Generated proto DO NOT EDIT */

export type SampleServiceService = typeof SampleServiceService;
export const SampleServiceService = {
  /** [webezyio] - None */
  sampleUnary: {
    path: "/SampleService/SampleUnary",
    requestStream: false,
    responseStream: false,
    requestSerialize: (value: SampleMessage) => Buffer.from(SampleMessage.encode(value).finish()),
    requestDeserialize: (value: Buffer) => SampleMessage.decode(value),
    responseSerialize: (value: SampleMessage) => Buffer.from(SampleMessage.encode(value).finish()),
    responseDeserialize: (value: Buffer) => SampleMessage.decode(value),
  },
} as const;

export interface SampleServiceServer extends UntypedServiceImplementation {
  /** [webezyio] - None */
  sampleUnary: handleUnaryCall<SampleMessage, SampleMessage>;
}

export interface SampleServiceClient extends Client {
  /** [webezyio] - None */
  sampleUnary(
    request: SampleMessage,
    callback: (error: ServiceError | null, response: SampleMessage) => void,
  ): ClientUnaryCall;
  sampleUnary(
    request: SampleMessage,
    metadata: Metadata,
    callback: (error: ServiceError | null, response: SampleMessage) => void,
  ): ClientUnaryCall;
  sampleUnary(
    request: SampleMessage,
    metadata: Metadata,
    options: Partial<CallOptions>,
    callback: (error: ServiceError | null, response: SampleMessage) => void,
  ): ClientUnaryCall;
}

export const SampleServiceClient = makeGenericClientConstructor(SampleServiceService, "SampleService") as unknown as {
  new (address: string, credentials: ChannelCredentials, options?: Partial<ChannelOptions>): SampleServiceClient;
  service: typeof SampleServiceService;
};
