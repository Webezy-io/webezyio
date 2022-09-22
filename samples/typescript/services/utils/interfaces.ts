// Insert here more interfaces to service will be able to speak with
interface Api<T> {
	[method: string]: T;
}

export type ApiType<T> = Api<T> & {

}