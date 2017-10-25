from typing import List, Dict

import discord

from command import CommandHandler, Command


class Module:
    def __init__(self, name: str, channels: List[discord.Channel], commands: List[Command]):
        self.name = name
        self.channels = channels
        self.commands = self.create_module_dict(commands)
        self.admin_only = False

    def create_module_dict(self, commands: List[Command]) -> Dict[str, Command]:
        result = {}
        for command in commands:
            result[command.name] = command

        return result

    def get_name(self) -> str:
        return self.name

    def add_channel(self, channel: discord.Channel):
        self.channels.append(channel)

    def has_channel(self, member: discord.Member, channel: discord.Channel) -> bool:
        if channel.permissions_for(member).administrator:
            if self.admin_only:
                return True

        return channel in self.channels

    def has_command(self, command: str) -> bool:
        return command in self.commands

    async def setup(self, client: discord.Client):
        pass

    async def run_command(self, command: str, client: discord.Client, message: discord.Message, arguments: str):
        await self.commands[command].handle(client, message, arguments)
