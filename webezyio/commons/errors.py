# Copyright (c) 2022 Webezy.io.

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

class WebezyCoderError(Exception):
    """Exception raised for errors in the input salary.

    Attributes:
        error -- Which error type
        message -- explanation of the error
    """

    def __init__(self, error, message="Unknown webezy error"):
        self.error = error
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'[{self.error}] {self.message}'


class WebezyProtoError(Exception):
    """Exception raised for errors in the proto parse process.

    Attributes:
        resource -- Which resource the error is triggered on
        message -- explanation of the error
    """

    def __init__(self, resource, message="Error occured during parsing of proto file"):
        self.resource = resource
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'[{self.resource}] {self.message}'


class WebezyValidationError(Exception):

    def __init__(self, resource, message="Error occured during parsing of proto type"):
        self.resource = resource
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'[{self.resource}] {self.message}'
