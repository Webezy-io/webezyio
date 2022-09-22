interface Api<T> {
    [method: string]: T;
}
export declare type ApiType<T> = Api<T> & {};
export {};
