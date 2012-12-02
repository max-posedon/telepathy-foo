from telepathy.server import ConnectionManager

from foo import PROGRAM, PROTOCOL
from foo.protocol import FooProtocol

__all__ = (
	'FooConnectionManager',
)


class FooConnectionManager(ConnectionManager):
    def __init__(self, shutdown_func=None):
        ConnectionManager.__init__(self, PROGRAM)
        self._implement_protocol(PROTOCOL, FooProtocol)
