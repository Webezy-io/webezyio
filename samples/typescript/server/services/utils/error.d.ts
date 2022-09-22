import { Metadata, ServiceError as grpcServiceError, status } from '@grpc/grpc-js';
export declare class ServiceError extends Error implements Partial<grpcServiceError> {
    code: status;
    message: string;
    details?: string | undefined;
    metadata?: Metadata | undefined;
    name: string;
    constructor(code: status, message: string, details?: string | undefined, metadata?: Metadata | undefined);
}
