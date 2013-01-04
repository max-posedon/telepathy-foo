import gobject
from dbus.types import Dictionary
from dbus.service import method
import weakref

from telepathy.constants import (
    CONNECTION_STATUS_CONNECTED,
    CONNECTION_STATUS_DISCONNECTED,
    CONNECTION_STATUS_REASON_REQUESTED,
    CONNECTION_STATUS_REASON_NONE_SPECIFIED,
    CONTACT_LIST_STATE_SUCCESS,
    HANDLE_TYPE_CONTACT,
    SUBSCRIPTION_STATE_YES,
)
from telepathy.interfaces import (
    CONNECTION,
    CONNECTION_INTERFACE_CONTACT_LIST,
    CONNECTION_INTERFACE_CONTACTS,
)
from telepathy.server import (
    Connection,
    ConnectionInterfaceRequests,
)
from telepathy.server.handle import Handle

from foo import PROGRAM, PROTOCOL, CONTACTS
from foo.conn_contact_list import ConnectionInterfaceContactList
from foo.conn_contacts import ConnectionInterfaceContacts
from foo.channel_manager import FooChannelManager


__all__ = (
    'FooConnection',
)


class FooConnection(Connection,
    ConnectionInterfaceContactList,
    ConnectionInterfaceContacts,
    ConnectionInterfaceRequests,
    ):

    def __init__(self, protocol, manager, parameters):
        protocol.check_parameters(parameters)
        self._manager = weakref.proxy(manager)

        account = unicode(parameters['account'])
        self._channel_manager = FooChannelManager(self, protocol)
        Connection.__init__(self, PROTOCOL, account, PROGRAM, protocol)
        ConnectionInterfaceContactList.__init__(self)
        ConnectionInterfaceContacts.__init__(self)
        ConnectionInterfaceRequests.__init__(self)

        self_handle = self.create_handle(HANDLE_TYPE_CONTACT, account.encode('utf-8'))
        self.set_self_handle(self_handle)

        self.__disconnect_reason = CONNECTION_STATUS_REASON_NONE_SPECIFIED

    def Connect(self):
        if self._status == CONNECTION_STATUS_DISCONNECTED:
            gobject.timeout_add(50, self._connected)

    def _connected(self):
        self.StatusChanged(CONNECTION_STATUS_CONNECTED, CONNECTION_STATUS_REASON_REQUESTED)
        self.ContactListStateChanged(CONTACT_LIST_STATE_SUCCESS)

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

    @method(CONNECTION_INTERFACE_CONTACT_LIST, in_signature='asb', out_signature='a{ua{sv}}', sender_keyword='sender')
    def GetContactListAttributes(self, interfaces, hold, sender):
        ret = Dictionary(signature='ua{sv}')
        for contact in CONTACTS:
            handle = self.ensure_handle(HANDLE_TYPE_CONTACT, contact)
            ret[int(handle)] = Dictionary(signature='sv')
            ret[int(handle)][CONNECTION + '/contact-id'] = contact
            ret[int(handle)][CONNECTION_INTERFACE_CONTACT_LIST + '/subscribe'] = SUBSCRIPTION_STATE_YES
            ret[int(handle)][CONNECTION_INTERFACE_CONTACT_LIST + '/publish'] = SUBSCRIPTION_STATE_YES
        return ret
