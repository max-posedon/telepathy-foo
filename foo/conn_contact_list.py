import dbus
import dbus.service

from telepathy.constants import CONTACT_LIST_STATE_NONE
from telepathy.interfaces import CONNECTION_INTERFACE_CONTACT_LIST
from telepathy.server.properties import DBusProperties

from telepathy._generated.Connection_Interface_Contact_List import ConnectionInterfaceContactList as _ConnectionInterfaceContactList


__all__ = (
    'ConnectionInterfaceContactList',
)


class ConnectionInterfaceContactList(_ConnectionInterfaceContactList, DBusProperties):

    def __init__(self):
        _ConnectionInterfaceContactList.__init__(self)
        DBusProperties.__init__(self)

        self._contact_list_state = CONTACT_LIST_STATE_NONE
        self._contact_list_persists = True
        self._can_change_contact_list = False
        self._request_uses_message = False
        self._download_at_connection = True

        self._implement_property_get(CONNECTION_INTERFACE_CONTACT_LIST, {
            'ContactListState': lambda: dbus.UInt32(self._get_contact_list_state()),
            'ContactListPersists': lambda: dbus.Boolean(self._get_contact_list_persists()),
            'CanChangeContactList': lambda: dbus.Boolean(self._get_can_change_contact_list)(),
            'RequestUsesMessage': lambda: dbus.Boolean(self._get_request_uses_message()),
            'DownloadAtConnection': lambda: dbus.Boolean(self._get_download_at_connection()),
        })

    @dbus.service.signal(CONNECTION_INTERFACE_CONTACT_LIST, signature='u')
    def ContactListStateChanged(self, contact_list_state):
        self._contact_list_state = contact_list_state

    def _get_contact_list_state(self):
        return self._contact_list_state

    def _get_contact_list_persist(self):
        return self._contact_list_persists

    def _get_can_change_contact_list(self):
        return self._can_change_contact_list

    def _get_request_uses_message(self):
        return self._request_uses_message

    def _get_download_at_connection(self):
        return self._download_at_connection
