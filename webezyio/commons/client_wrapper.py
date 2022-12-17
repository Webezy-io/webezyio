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

import grpc
import sys
from functools import partial
from webezyio.commons import pretty

class WebezyioClient:

    def __init__(self, service_module, stub_name, host, port, timeout=10):
        channel = grpc.insecure_channel('{0}:{1}'.format(host, port))
        self.timeout = timeout
        try:
            grpc.channel_ready_future(channel).result(timeout=self.timeout)
        except grpc.FutureTimeoutError:
            sys.exit('Error connecting to server')
        self.stub = getattr(service_module, stub_name)(channel)

    def __getattr__(self, attr):
        return partial(self._wrapped_call, self.stub, attr)

    # args[0]: stub, args[1]: function to call, args[2]: Request
    # kwargs: keyword arguments
    def _wrapped_call(self, *args, **kwargs):
        try:
            return getattr(args[0], args[1]).with_call(
                args[2], **kwargs, timeout=self.timeout
            )
        except grpc.RpcError as e:
            pretty.print_error('Call {0} failed with {1}'.format(
                args[1], e.code())
            )
            raise