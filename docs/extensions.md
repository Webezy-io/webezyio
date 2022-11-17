# Extensions in Webezy.io

`Protobuf` come with cool and powerful feature called ["Options"](https://developers.google.com/protocol-buffers/docs/proto#options).
This feature allow us to utulize it as "Extensioning" our default protobuf resources.

Custom extensions can be defined for every kind of construct in the `Protocol Buffers` language.
__Currently__ we support 3 types of extensions:
- FileOptions - Top level (Global) extensions for a `service` or `package` proto file.
- MessageOptions - A unique `message` extensions.
- FieldOptions - The most granular extension which can be attached to specific `fields` in each `message`

```proto
import "google/protobuf/descriptor.proto";

extend google.protobuf.FileOptions {
  optional string my_file_extension = 50000;
}
extend google.protobuf.MessageOptions {
  optional int32 my_message_extension = 50001;
}
extend google.protobuf.FieldOptions {
  optional float my_field_extension = 50002;
}

// [FileOptions] Global level for whole file (Service / Package)
option (my_file_extension) = "SomeToken";

message MyMessage {
  
  // [MessageOptions] A Message specific extension
  option (my_message_extension) = 1234;
  
  // [FieldOptions] A field specific extension
  optional int32 foo = 1 [(my_field_extension = 4.5];
}

```

> __Warning__ Extensions limitations:
  We have a strict rules on implementing a custom extension of yout own that __MUST__ be followed for supported feature and seemless integration with Webezy.io modules.

  - Extension must be wrapped to a __parent message__ - Meaning if you wish to extend you own custom functionality with `FieldOptions` you need to nest it inside a "normal" message that will encapsulate the extended type.

  - Extension fields __MUST__ be one of the following supported types:
    * String (+List)
    * Integer (+List)
    * Boolean (+List)
    * Enums (+List) 
    * Message (+List) *

  > __Note__ __*__ For nested messages will act properly as values in your extensions you cant place another `"Deep Nested"` message or special Map type.

## Examples

```proto
package domain.extensions.v1;

// 'FieldOptions' extensions are used inside messages for each field seperatly,
// Regardles of the field original type the extensions map for each field is stand-alone.
message TestExtension {
  string test_string = 1 [
    (domain.extensions.v1.ExtensionMessage.TestString) = "Some Test"
  ];
  int32 test_int = 2 [
    (domain.extensions.v1.ExtensionMessage.TestEnum) = SOME_VALUE
  ];
  bool test_bool = 3 [
    (domain.extensions.v1.ExtensionMessage.TestListBool) = true,
    (domain.extensions.v1.ExtensionMessage.TestListBool) = false
  ];
  double test_int_extension = 4 [
    (domain.extensions.v1.ExtensionMessage.TestInt) = 10
  ];
  domain.extensions.v1.TestEnum test_enum = 5 [
    (domain.extensions.v1.ExtensionMessage.TestMessage) = {
      name: "Hello extension"
    },
    (domain.extensions.v1.ExtensionMessage).messages = "Extensions",
    (domain.extensions.v1.ExtensionMessage).messages = "Are",
    (domain.extensions.v1.ExtensionMessage).messages = "Powerful"
  ];
}

message TestMessage {
  string name = 1;
  repeated messages = 2;
}

enum TestEnum {
  UNKNOWN = 0;
  SOME_VALUE = 1;
  SOME_OTHER_VALUE = 2;
}

// Defining parent message which holding extendable of 'FieldOptions'
message ExtensionMessage {
  extend google.protobuf.FieldOptions {
    repeated bool TestListBool = 55556;
    string TestString = 55557;
    int32 TestInt = 55559;
    domain.extensions.v1.TestEnum TestEnum = 55560;
    domain.extensions.v1.TestMessage TestMessage = 55561;
  }
}
```