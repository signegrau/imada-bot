import discord
import asyncio

from command import Command
from module import Module


class RoleAssigner(Module):
    def __init__(self, config: dict):
        super().__init__('roleassigner',  "Assigning roles to users", [], [
            Command('join', 'join a role', self.join),
            Command('leave', 'leave a role', self.leave),
            Command('roleslist', 'list available roles', self.list),
            Command('rolesadd', 'add roles to make available to join', self.add_role, admin_required=True),
            Command('rolesremove', 'remove roles from available roles', self.remove_role, admin_required=True)
        ])

        self.config = config

        self.roles = self.config.get('roles', {})

    async def join(self, client: discord.Client, message: discord.Message, arguments: str):
        role_text = arguments.lower()
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
        role_text = arguments.lower()
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

    async def list(self, client: discord.Client, message: discord.Message, arguments: str):
        if len(self.roles) > 0:
            message_string = '```\nAvailable roles:'

            for role_text in self.roles:
                role = discord.utils.get(message.server.roles, id=self.roles[role_text])
                message_string += '\n\t' + role.name

            message_string += "```"

            await client.send_message(message.channel, message_string)
        else:
            await client.send_message(message.channel, 'No roles to join 😕')

    def sync_config(self):
        self.config['roles'] = self.roles

    async def add_role(self, client: discord.Client, message: discord.Message, arguments: str):
        roles = message.role_mentions

        if len(roles) < 1:
            await client.send_message(message.channel, 'Cannot add `NullPointerException` to roles')
        elif len(roles) == 1:
            role = roles[0]
            if role.name.lower() not in self.roles:
                self.roles[role.name.lower()] = role.id
                await client.send_message(message.channel, f'Added role `{role.name}`')
            else:
                await client.send_message(message.channel, f'Role already available')

            self.sync_config()
            client.save_module_config(self.name, self.config)
        else:
            # Was this so important?
            message_text = '```\nAdded roles:'
            some_role_not_added = False
            for role in roles:
                if role.name.lower() not in self.roles:
                    self.roles[role.name.lower()] = role.id
                    message_text += f'\n\t{role.name}'
                else:
                    some_role_not_added = True

            if some_role_not_added:
                message_text += '\n\nOthers are already available'

            message_text += '\n```'
            await client.send_message(message.channel, message_text)

            self.sync_config()
            client.save_module_config(self.name, self.config)

    async def remove_role(self, client: discord.Client, message: discord.Message, arguments: str):
        roles = message.role_mentions

        if len(roles) < 1:
            await client.send_message(message.channel, 'Cannot remove `NullPointerException` from roles')
        else:
            role = roles[0]
            if role.name in self.roles:
                del self.roles[role.name.lower()]
                await client.send_message(message.channel, f'Removed role `{role.name}`')
            else:
                await client.send_message(message.channel, f'Role is not available')

            self.sync_config()
            client.save_module_config(self.name, self.config)
