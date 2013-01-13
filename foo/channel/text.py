from time import time
from uuid import uuid4

import gobject
from dbus.types import Array, Dictionary, String, UInt32, UInt64

from telepathy.constants import CHANNEL_TEXT_MESSAGE_TYPE_NORMAL
from telepathy.server import ChannelTypeText, ChannelInterfaceMessages


__all__ = (
    'FooTextChannel',
)


class FooTextChannel(ChannelTypeText, ChannelInterfaceMessages):
    _supported_content_types = ['text/plain']

    def __init__(self, conn, manager, props, object_path=None):
        _, surpress_handler, handle = manager._get_type_requested_handle(props)
        self.handle = handle
        self.__message_received_id = 0

        ChannelTypeText.__init__(self, conn, manager, props, object_path)
        ChannelInterfaceMessages.__init__(self)

    def SendMessage(self, message, flags):
        token = str(uuid4())
        gobject.timeout_add(50, self._send_message, message, flags, token)
        return token

    def _send_message(self, message, flags, token):
        headers = Dictionary({
            String('message-sent'): UInt64(time()),
            String('message-type'): UInt32(CHANNEL_TEXT_MESSAGE_TYPE_NORMAL),
        }, signature='sv')
        body = Dictionary({
            String('content-type'): String('text/plain'),
            String('content'): message[1]['content'],
        }, signature='sv')
        message = Array([headers, body], signature='a{sv}')
        self.MessageSent(message, flags, String(token))

        gobject.timeout_add(50, self._message_received, str(message[1]['content']))

    def _message_received(self, msg):
        self.__message_received_id += 1
        header = Dictionary({
            'pending-message-id': UInt32(self.__message_received_id),
            'message-received': UInt64(time()),
            'message-type': UInt32(CHANNEL_TEXT_MESSAGE_TYPE_NORMAL),
            'sender-nickname': String(self.handle.get_name()),
            }, signature='sv')
        body = Dictionary({
            String('content-type'): String('text/plain'),
            String('content'): String(msg),
        }, signature='sv')
        message = Array([header, body], signature='a{sv}')
        self.MessageReceived(message)
