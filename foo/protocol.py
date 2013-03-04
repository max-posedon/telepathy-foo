from dbus.types import String, UInt32

from telepathy.constants import (
    CONNECTION_PRESENCE_STATUS_AVAILABLE,
    CONNECTION_PRESENCE_STATUS_OFFLINE,
    CONNECTION_PRESENCE_TYPE_AVAILABLE,
    CONNECTION_PRESENCE_TYPE_OFFLINE,
    HANDLE_TYPE_CONTACT,
)
from telepathy.interfaces import (
    CHANNEL,
    CHANNEL_TYPE_TEXT,
    CONNECTION_INTERFACE_ALIASING,
    CONNECTION_INTERFACE_AVATARS,
    CONNECTION_INTERFACE_BALANCE,
    CONNECTION_INTERFACE_CONTACT_GROUPS,
    CONNECTION_INTERFACE_CONTACT_LIST,
    CONNECTION_INTERFACE_CONTACT_INFO,
    CONNECTION_INTERFACE_CONTACTS,
    CONNECTION_INTERFACE_REQUESTS,
    CONNECTION_INTERFACE_SIMPLE_PRESENCE,
)
from telepathy.server import (
    Protocol,
    ProtocolInterfaceAvatars,
    ProtocolInterfacePresence,
)

from foo import PROTOCOL, AVATAR_MIME
from foo.connection import FooConnection


__all__ = (
    'FooProtocol',
)


class FooProtocol(Protocol, ProtocolInterfacePresence, ProtocolInterfaceAvatars):
    
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
        CONNECTION_INTERFACE_ALIASING,
        CONNECTION_INTERFACE_AVATARS,
        CONNECTION_INTERFACE_BALANCE,
        CONNECTION_INTERFACE_CONTACT_GROUPS,
        CONNECTION_INTERFACE_CONTACT_INFO,
        CONNECTION_INTERFACE_CONTACT_LIST,
        CONNECTION_INTERFACE_CONTACTS,
        CONNECTION_INTERFACE_REQUESTS,
        CONNECTION_INTERFACE_SIMPLE_PRESENCE,
    ]

    _statuses = {
        CONNECTION_PRESENCE_STATUS_AVAILABLE: (
            CONNECTION_PRESENCE_TYPE_AVAILABLE,
            True,
            True,
        ),
        CONNECTION_PRESENCE_STATUS_OFFLINE: (
            CONNECTION_PRESENCE_TYPE_OFFLINE,
            True,
            False,
        ),
    }

    _supported_avatar_mime_types = [AVATAR_MIME]

    def __init__(self, connection_manager):
        Protocol.__init__(self, connection_manager, PROTOCOL)
        ProtocolInterfaceAvatars.__init__(self)
        ProtocolInterfacePresence.__init__(self)

    def create_connection(self, connection_manager, parameters):
        return FooConnection(self, connection_manager, parameters)
