import discord
import asyncio
from discord_token import get_token
from testmodule import testmodule
from roleassigner import roleassigner


class imadabot(discord.Client):
    def __init__(self):
        super(imadabot, self).__init__()
        self.testing_channel = None

        self.modules = [
            testmodule(),
            roleassigner()
        ]
        
    def run(self, token):
        super(imadabot, self).run(token)

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if not message.content.startswith('!'):
            return

        command, _, arguments = message.content.partition(' ')
        command = command[1:].lower()
        arguments = arguments.strip()

        modules = self.get_loaded_modules(message.channel)

        for module in modules:
            if module.has_command(command):
                await module.run_command(command, self, message, arguments)

        if command == 'channelload':
            if message.channel.permissions_for(message.author).administrator:
                module = self.get_module(arguments)

                if module:
                    module.add_channel(message.channel)
                    await self.send_message(message.channel, 'This is the testing channel')
                else:
                    await self.send_message(message.channel, f'No module named `{arguments}`')
            else:
                await self.send_message(message.channel, 'Only a administrator can do that')

    def get_loaded_modules(self, channel):
        modules = []

        for module in self.modules:
            if module.has_channel(channel):
                modules.append(module)

        return modules

    def get_module(self, name):
        for module in self.modules:
            if module.name == name:
                return module

        return None


if __name__ == "__main__":
    bot = imadabot()
    bot.run(get_token())
