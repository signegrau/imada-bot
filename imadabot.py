import json

import discord

from discord_token import get_token
from modules.roleassigner import roleassigner
from modules.testmodule import testmodule


class imadabot(discord.Client):
    def __init__(self):
        super(imadabot, self).__init__()

        self.config = {}
        with open('config.json', 'r', encoding='utf8') as file:
            self.config = json.loads(file.read())

        self.modules = [
            testmodule(),
            roleassigner(self.config['roleassigner'])
        ]
        
    def run(self, token):
        super(imadabot, self).run(token)

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

        for module in self.modules:
            if module.name in self.config:
                for channel_id in self.config[module.name]['channels']:
                    channel = self.get_channel(channel_id)
                    module.add_channel(channel)

        for module in self.modules:
            await module.setup(self)

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

        if command == 'channeladd':
            if message.channel.permissions_for(message.author).administrator:
                module = self.get_module(arguments)

                if module and not module.has_channel(message.channel):
                    module.add_channel(message.channel)
                    if arguments not in self.config:
                        self.config[arguments] = {
                            'channels': []
                        }

                    self.config[arguments]['channels'].append(message.channel.id)
                    await self.send_message(message.channel, f'Added modules `{arguments}` to `{message.channel.name}`')
                    self.save_config()
                else:
                    await self.send_message(message.channel,
                                            f'No module named `{arguments}` or already added to channel')
            else:
                await self.send_message(message.channel, 'Only a administrator can do that')

    def save_config(self):
        with open('config.json', 'w', encoding='utf8') as file:
            file.write(json.dumps(self.config, indent=4))

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
