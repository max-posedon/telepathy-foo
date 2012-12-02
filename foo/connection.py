import weakref
import gobject

from telepathy import (
    CONNECTION_STATUS_CONNECTED,
    CONNECTION_STATUS_DISCONNECTED,
    CONNECTION_STATUS_REASON_REQUESTED,
    CONNECTION_STATUS_REASON_NONE_SPECIFIED,
    HANDLE_TYPE_CONTACT,
    )
from telepathy.server import Connection

from foo import PROGRAM, PROTOCOL


__all__ = (
    'FooConnection',
)


class FooConnection(Connection):

    def __init__(self, protocol, manager, parameters):
        protocol.check_parameters(parameters)
        account = unicode(parameters['account'])

        self._manager = weakref.proxy(manager)
        Connection.__init__(self, PROTOCOL, account, PROGRAM, protocol)

        self_handle = self.create_handle(HANDLE_TYPE_CONTACT, account.encode('utf-8'))
        self.set_self_handle(self_handle)

        self.__disconnect_reason = CONNECTION_STATUS_REASON_NONE_SPECIFIED

    def Connect(self):
        if self._status == CONNECTION_STATUS_DISCONNECTED:
            gobject.timeout_add(50, self._connected)

    def _connected(self):
        self.StatusChanged(CONNECTION_STATUS_CONNECTED, CONNECTION_STATUS_REASON_REQUESTED)
