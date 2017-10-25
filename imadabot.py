from typing import List

import asyncio
import json
from pathlib import Path

import discord
from discord_token import get_token

from module import Module
from modules.modulemanager import ModuleManager
from modules.roleassigner import RoleAssigner
from modules.testmodule import TestModule


class ImadaBot(discord.Client):
    def __init__(self):
        super(ImadaBot, self).__init__()

        self.config = {}

        config_file = Path('config.json')
        if config_file.is_file():
            with config_file.open('r', encoding='utf8') as file:
                self.config = json.loads(file.read())
        else:
            self.config = {

            }

        self.modules = [
            TestModule(),
            RoleAssigner(self.config.get('roleassigner', {})),
            ModuleManager()
        ]

    def run(self, token: str):
        super(ImadaBot, self).run(token)

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

    async def on_message(self, message: discord.Message):
        if not message.content.startswith('!'):
            return

        command, _, arguments = message.content.partition(' ')
        command = command[1:].lower()
        arguments = arguments.strip()

        modules = self.get_loaded_modules(message.author, message.channel)

        for module in modules:
            if module.has_command(command):
                await module.run_command(command, self, message, arguments)

    def save_config(self):
        with open('config.json', 'w', encoding='utf8') as file:
            file.write(json.dumps(self.config, indent=4))

    def get_loaded_modules(self, member: discord.Member, channel: discord.Channel) -> List[Module]:
        modules = []

        for module in self.modules:
            if module.has_channel(member, channel):
                modules.append(module)

        return modules

    def get_module(self, name: str):
        for module in self.modules:
            if module.name == name:
                return module

        return None


if __name__ == "__main__":
    bot = ImadaBot()
    bot.run(get_token())
