from telepathy._generated.Connection_Interface_Contacts import ConnectionInterfaceContacts as _ConnectionInterfaceContacts
from telepathy.interfaces import CONNECTION, CONNECTION_INTERFACE_CONTACTS
from telepathy.server.properties import DBusProperties


__all__ = (
    'ConnectionInterfaceContacts',
)


class ConnectionInterfaceContacts(_ConnectionInterfaceContacts, DBusProperties):

    _contact_attribute_interfaces = {
        CONNECTION: 'contact-id',
    }

    def __init__(self):
        _ConnectionInterfaceContacts.__init__(self)
        DBusProperties.__init__(self)

        self._implement_property_get(CONNECTION_INTERFACE_CONTACTS, {
            'ContactAttributeInterfaces': self.get_contact_attribute_interfaces,
        })

    def get_contact_attribute_interfaces(self):
        return self._contact_attribute_interfaces.keys()

