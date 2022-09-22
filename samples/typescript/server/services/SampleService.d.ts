import { handleUnaryCall, UntypedHandleCall } from '@grpc/grpc-js';
import { ApiType } from './utils/interfaces';
import { SampleServiceServer, SampleServiceService } from './protos/SampleService';
import * as SamplePackage from './protos/SamplePackage';
declare class SampleService implements SampleServiceServer, ApiType<UntypedHandleCall> {
    [method: string]: any;
    sampleUnary: handleUnaryCall<SamplePackage.SampleMessage, SamplePackage.SampleMessage>;
}
export { SampleService, SampleServiceService };
