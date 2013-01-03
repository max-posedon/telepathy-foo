import gobject
from dbus.types import Dictionary
from dbus.service import method
import weakref

from telepathy.constants import (
    CONNECTION_STATUS_CONNECTED,
    CONNECTION_STATUS_DISCONNECTED,
    CONNECTION_STATUS_REASON_REQUESTED,
    CONNECTION_STATUS_REASON_NONE_SPECIFIED,
    HANDLE_TYPE_CONTACT,
)
from telepathy.interfaces import CONNECTION, CONNECTION_INTERFACE_CONTACTS
from telepathy.server import (
    Connection,
    ConnectionInterfaceRequests,
)

from foo import PROGRAM, PROTOCOL
from foo.conn_contacts import ConnectionInterfaceContacts
from foo.channel_manager import FooChannelManager


__all__ = (
    'FooConnection',
)


class FooConnection(Connection,
    ConnectionInterfaceContacts,
    ConnectionInterfaceRequests,
    ):

    def __init__(self, protocol, manager, parameters):
        protocol.check_parameters(parameters)
        account = unicode(parameters['account'])

        self._manager = weakref.proxy(manager)
        self._channel_manager = FooChannelManager(self, protocol)

        Connection.__init__(self, PROTOCOL, account, PROGRAM, protocol)
        ConnectionInterfaceRequests.__init__(self)
        ConnectionInterfaceContacts.__init__(self)

        self_handle = self.create_handle(HANDLE_TYPE_CONTACT, account.encode('utf-8'))
        self.set_self_handle(self_handle)

        self.__disconnect_reason = CONNECTION_STATUS_REASON_NONE_SPECIFIED

    def Connect(self):
        if self._status == CONNECTION_STATUS_DISCONNECTED:
            gobject.timeout_add(50, self._connected)

    def _connected(self):
        self.StatusChanged(CONNECTION_STATUS_CONNECTED, CONNECTION_STATUS_REASON_REQUESTED)

    def Disconnect(self):
        self.__disconnect_reason = CONNECTION_STATUS_REASON_REQUESTED
        gobject.timeout_add(50, self._disconnected)

    def _disconnected(self):
        self.StatusChanged(CONNECTION_STATUS_DISCONNECTED, self.__disconnect_reason)
        self._manager.disconnected(self)

    @method(CONNECTION_INTERFACE_CONTACTS, in_signature='auasb', out_signature='a{ua{sv}}', sender_keyword='sender')
    def GetContactAttributes(self, handles, interfaces, hold, sender):
        supported_interfaces = set()
        for interface in interfaces:
            if interface in self.attributes:
                supported_interfaces.add(interface)

        handle_type = HANDLE_TYPE_CONTACT
        ret = Dictionary(signature='ua{sv}')
        for handle in handles:
            ret[handle] = Dictionary(signature='sv')

        functions = {
            CONNECTION: lambda x: zip(x, self.InspectHandles(handle_type, x)),
        }

        if hold:
            self.HoldHandles(handle_type, handles, sender)
        supported_interfaces.add(CONNECTION)

        for interface in supported_interfaces:
            interface_attribute = interface + '/' + self._contact_attribute_interfaces[interface]
            results = functions[interface](handles)
            for handle, value in results:
                ret[int(handle)][interface_attribute] = value

        return ret
