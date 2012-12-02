from telepathy.server import Protocol

from foo import PROTOCOL
from foo.connection import FooConnection


__all__ = (
    'FooProtocol',
)


class FooProtocol(Protocol):
    
    _proto = PROTOCOL
    _english_name = "Foo"
    _icon = "im-foo"
    _vcard_field = "im-bar"

    _mandatory_parameters = {
        'account': 's',
    }

    def __init__(self, connection_manager):
        Protocol.__init__(self, connection_manager, PROTOCOL)

    def create_connection(self, connection_manager, parameters):
        return FooConnection(self, connection_manager, parameters)
