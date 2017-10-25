import asyncio
from typing import List, Dict

import discord

from command import CommandHandler, Command


class Module:
    def __init__(self, name: str, description: str, channels: List[discord.Channel], commands: List[Command]):
        self.name = name
        self.description = description
        self.channels = channels
        self.commands = self.create_module_dict(commands)
        self.admin_module = False

    def create_module_dict(self, commands: List[Command]) -> Dict[str, Command]:
        result = {}
        for command in commands:
            result[command.name] = command

        return result

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description

    def add_channel(self, channel: discord.Channel):
        self.channels.append(channel)

    def remove_channel(self, channel: discord.Channel):
        self.channels.remove(channel)

    def has_channel(self, member: discord.Member, channel: discord.Channel) -> bool:
        if channel.permissions_for(member).administrator:
            if self.admin_module:
                return True

        return channel in self.channels

    def has_command(self, command: str) -> bool:
        return command in self.commands

    async def setup(self, client: discord.Client):
        pass

    async def run_command(self, command: str, client: discord.Client, message: discord.Message, arguments: str):
        admin_required = self.admin_module or self.commands[command].admin_required
        if admin_required and not message.channel.permissions_for(message.author).administrator:
            warning = await client.send_message(message.channel, f'{message.author.mention} is not in the sudoers '
                                                                 f'file. This incident will be reported.')
            await asyncio.sleep(60)
            await client.delete_message(warning)
        else:
            await self.commands[command].handle(client, message, arguments)
