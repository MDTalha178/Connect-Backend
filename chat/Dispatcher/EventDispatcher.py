class EventDispatcher:

    def __init__(self, channel_layer, room):
        self.channel_layer = channel_layer
        self.group_name = room

    async def channel_event_dispatch(self, **kwargs):
        await self.channel_layer.group_add(
            self.group_name,
            kwargs.get('channel_name')
        )
