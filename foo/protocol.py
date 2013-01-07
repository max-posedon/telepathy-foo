from dbus.types import String, UInt32

from telepathy.constants import HANDLE_TYPE_CONTACT
from telepathy.interfaces import (
    CHANNEL,
    CHANNEL_TYPE_TEXT,
    CONNECTION_INTERFACE_CONTACT_LIST,
    CONNECTION_INTERFACE_CONTACTS,
    CONNECTION_INTERFACE_REQUESTS,
)
from telepathy.server import Protocol

from foo import PROTOCOL
from foo.connection import FooConnection


__all__ = (
    'FooProtocol',
)


class FooProtocol(Protocol):
    
    _proto = PROTOCOL
    _english_name = PROTOCOL.capitalize()
    _icon = "im-%s" % PROTOCOL
    _vcard_field = "im-%s" % PROTOCOL

    _mandatory_parameters = {
        'account': 's',
    }

    _requestable_channel_classes = [
        (
            {
                CHANNEL + '.ChannelType': String(CHANNEL_TYPE_TEXT),
                CHANNEL + '.TargetHandleType': UInt32(HANDLE_TYPE_CONTACT),
            },
            [
                CHANNEL + '.TargetHandle',
                CHANNEL + '.TargetID',
            ]
        ),
    ]

    _supported_interfaces = [
        CONNECTION_INTERFACE_CONTACT_LIST,
        CONNECTION_INTERFACE_CONTACTS,
        CONNECTION_INTERFACE_REQUESTS,
    ]

    def __init__(self, connection_manager):
        Protocol.__init__(self, connection_manager, PROTOCOL)

    def create_connection(self, connection_manager, parameters):
        return FooConnection(self, connection_manager, parameters)
