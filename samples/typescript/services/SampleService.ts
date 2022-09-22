import { 
	handleUnaryCall,
	handleClientStreamingCall,
	handleServerStreamingCall,
	handleBidiStreamingCall,
	sendUnaryData,
	ServerDuplexStream,
	ServerReadableStream,
	ServerUnaryCall,
	ServerWritableStream,
	status,
	UntypedHandleCall,
	Metadata
 } from '@grpc/grpc-js';
import { ServiceError } from './utils/error';
import { ApiType } from './utils/interfaces';
import { SampleServiceServer, SampleServiceService } from './protos/SampleService';
import * as SamplePackage from './protos/SamplePackage';

class SampleService implements SampleServiceServer, ApiType<UntypedHandleCall> {
	[method: string]: any;

	// @rpc @@webezyio - DO NOT REMOVE
	public sampleUnary: handleUnaryCall<SamplePackage.SampleMessage, SamplePackage.SampleMessage> = (
		call: ServerUnaryCall<SamplePackage.SampleMessage, SamplePackage.SampleMessage>,
		callback: sendUnaryData<SamplePackage.SampleMessage>
	) => {
		// let response:SamplePackage.SampleMessage = { SampleString: "SomeString" };
		// callback(null,response);
		callback(new ServiceError(status.UNIMPLEMENTED,"Method is not yet implemented"))
	}


}

export {
	SampleService,
	SampleServiceService
};