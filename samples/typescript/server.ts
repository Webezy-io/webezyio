// Webezy.io Generated Server Code
import { Server, ServerCredentials } from '@grpc/grpc-js';
import { SampleService, SampleServiceService } from './services/SampleService';

let _PORT:number = 50051;
let _HOST:string = '0.0.0.0';
let _ADDR = `${_HOST}:${_PORT}`
const server = new Server({
	"grpc.max_receive_message_length": -1,
	"grpc.max_send_message_length": -1,
});

server.addService(SampleServiceService, new SampleService());

server.bindAsync(_ADDR, ServerCredentials.createInsecure(), (err: Error | null, bindPort: number) => {
	if (err) {
		throw err;
	}

	console.log(`[webezy] Starting gRPC:server:${bindPort}`,`at -> ${new Date().toLocaleString()})`);
	server.start();
});