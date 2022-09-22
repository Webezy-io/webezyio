import { credentials, Metadata, ServiceError as _service_error, ClientUnaryCall, ClientDuplexStream, ClientReadableStream, ClientWritableStream } from '@grpc/grpc-js';
import { promisify } from 'util';
import { Observable } from 'rxjs';
import { SampleServiceClient } from './protos/SampleService'
import * as SamplePackage from './protos/SamplePackage'
const _DEFAULT_OPTION = {
	"grpc.keepalive_time_ms": 120000,
	"grpc.http2.min_time_between_pings_ms": 120000,
	"grpc.keepalive_timeout_ms": 20000,
	"grpc.http2.max_pings_without_data": 0,
	"grpc.keepalive_permit_without_calls": 1,
}

export class typescript {

	constructor(host: string = "localhost", port: number = 50051, metadata: Metadata = new Metadata()) {
		this.host = host;
		this.port = port;
		this.metadata = metadata;
		this.SampleService_client = new SampleServiceClient(`${this.host}:${this.port}`, credentials.createInsecure(),_DEFAULT_OPTION);
	}

	private readonly metadata: Metadata;
	private readonly host: string;
	private readonly port: number;
	private readonly SampleService_client: SampleServiceClient;

	
	public SampleUnary(request: SamplePackage.SampleMessage, metadata: Metadata): Promise<SamplePackage.SampleMessage>;
	public SampleUnary(request: SamplePackage.SampleMessage, metadata: Metadata, callback: (error: _service_error | null, response: SamplePackage.SampleMessage) => void): ClientUnaryCall;
	public SampleUnary(request: SamplePackage.SampleMessage, metadata: Metadata = this.metadata, callback?: (error: _service_error | null, response: SamplePackage.SampleMessage) => void): ClientUnaryCall | Promise<SamplePackage.SampleMessage> {
		if (callback === undefined) {
			return promisify<SamplePackage.SampleMessage, Metadata, SamplePackage.SampleMessage>(this.SampleService_client.sampleUnary.bind(this.SampleService_client))(request, metadata);
		} else {
		 return this.SampleService_client.sampleUnary(request, metadata, callback);
		}
	}
}
