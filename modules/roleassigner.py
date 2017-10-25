import discord
import asyncio

from command import Command
from module import Module


class RoleAssigner(Module):
    def __init__(self, config: dict):
        super().__init__('roleassigner', [], [
            Command('join', 'join a role', self.join),
            Command('leave', 'leave a role', self.leave)
        ])

        self.config = config

        self.roles = self.config['roles']

    async def join(self, client: discord.Client, message: discord.Message, arguments: str):
        role_text = arguments[:6].lower()
        member = message.author

        if role_text in self.roles:
            role = discord.utils.get(message.server.roles, id=self.roles[role_text])

            if role not in message.author.roles:
                await client.add_roles(member, role)
                await client.add_reaction(message, '👍')
            else:
                await client.add_reaction(message, '👀')
        else:
            await client.add_reaction(message, '❌')

    async def leave(self, client: discord.Client, message: discord.Message, arguments: str):
        role_text = arguments[:6].lower()
        member = message.author

        if role_text in self.roles:
            role = discord.utils.get(message.server.roles, id=self.roles[role_text])

            if role in message.author.roles:
                await client.remove_roles(member, role)
                await client.add_reaction(message, '👍')
            else:
                await client.add_reaction(message, '👀')
        else:
            await client.add_reaction(message, '❌')

    async def add_role(self, client: discord.Client, message: discord.Message, arguments: str):
        if not message.channel.permissions_for(message.author).administrator:
            warning = await client.send_message(message.channel, f'{message.author.mention} is not in the sudoers '
                                                                 f'file. This incident will be reported.')
            await asyncio.sleep(60)
            await client.delete_message(warning)
            return


