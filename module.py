import asyncio
from typing import List, Dict

import discord

from command import CommandHandler, Command


class Module:
    def __init__(self, name: str, description: str, channels: List[discord.Channel], commands: List[Command],
                 admin_module=False, global_module=False):
        self.name = name
        self.description = description
        self.channels = channels
        self.commands = self.create_module_dict(commands)
        self.admin_module = admin_module
        self.global_module = global_module

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
        if not self.admin_module and self.global_module:
            return True

        if channel.permissions_for(member).administrator:
            if self.admin_module:
                return True

        return channel in self.channels

    def has_command(self, command: str) -> bool:
        return command in self.commands

    async def setup(self, client: discord.Client):
        pass

    def get_commands(self, member: discord.Member, channel: discord.Channel):
        result = []

        for command in self.commands.values():
            admin_required = self.admin_module or command.admin_required

            if not admin_required or channel.permissions_for(member).administrator:
                result.append(command)

        return result


    async def run_command(self, command: str, client: discord.Client, message: discord.Message, arguments: str):
        admin_required = self.admin_module or self.commands[command].admin_required
        if admin_required and not message.channel.permissions_for(message.author).administrator:
            warning = await client.send_message(message.channel, f'{message.author.mention} is not in the sudoers '
                                                                 f'file. This incident will be reported.')
            await asyncio.sleep(60)
            await client.delete_message(warning)
        else:
            await self.commands[command].handle(client, message, arguments)
