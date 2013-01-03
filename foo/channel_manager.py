from telepathy.server import ChannelManager


__all__ = (
    'FooChannelManager',
)


class FooChannelManager(ChannelManager):

    def __init__(self, connection, protocol):
        ChannelManager.__init__(self, connection)
        self.set_requestable_channel_classes(protocol.requestable_channels)
