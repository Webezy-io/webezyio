import { Metadata, ServiceError as _service_error, ClientUnaryCall } from '@grpc/grpc-js';
import * as SamplePackage from './protos/SamplePackage';
export declare class typescript {
    constructor(host?: string, port?: number, metadata?: Metadata);
    private readonly metadata;
    private readonly host;
    private readonly port;
    private readonly SampleService_client;
    SampleUnary(request: SamplePackage.SampleMessage, metadata: Metadata): Promise<SamplePackage.SampleMessage>;
    SampleUnary(request: SamplePackage.SampleMessage, metadata: Metadata, callback: (error: _service_error | null, response: SamplePackage.SampleMessage) => void): ClientUnaryCall;
}
