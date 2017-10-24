class commandmodule:
    def __init__(self, name, channels, commands):
        self.name = name
        self.channels = channels
        self.commands = commands

    def get_name(self):
        return self.name

    def add_channel(self, channel):
        self.channels.append(channel)

    def has_channel(self, channel):
        return channel in self.channels

    def has_command(self, command):
        return command in self.commands

    async def run_command(self, command, client, message, arguments):
        await self.commands[command](client, message, arguments)
