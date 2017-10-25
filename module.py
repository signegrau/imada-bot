class Module:
    def __init__(self, name, channels, commands):
        self.name = name
        self.channels = channels
        self.commands = commands
        self.admin_only = False

    def get_name(self):
        return self.name

    def add_channel(self, channel):
        self.channels.append(channel)

    def add_channels(self, **channels):
        for channel in channels:
            self.add_channel(channel)

    def has_channel(self, member, channel):
        """
        :type member: discord.Member
        :type channel: discord.Channel
        :rtype : bool
        """
        if channel.permissions_for(member).administrator:
            if self.admin_only:
                return True

        return channel in self.channels

    def has_command(self, command):
        return command in self.commands

    async def setup(self, client):
        pass

    async def run_command(self, command, client, message, arguments):
        await self.commands[command](client, message, arguments)
