import asyncio

import discord

from command import Command
from module import Module


class ModuleManager(Module):
    def __init__(self):
        super(ModuleManager, self).__init__('modulemanager', [], [
            Command('channeladd', 'Add a module to channel', self.channel_add),
            Command('moduleslist', 'List available modules', self.channel_list)
        ])

        self.admin_only = True

    async def channel_add(self, client: discord.Client, message: discord.Message, arguments: str):
        if message.channel.permissions_for(message.author).administrator:
            module = client.get_module(arguments)

            if module and not module.has_channel(message.author, message.channel):
                module.add_channel(message.channel)
                if arguments not in client.config:
                    client.config[arguments] = {
                        'channels': []
                    }

                client.config[arguments]['channels'].append(message.channel.id)
                await client.send_message(message.channel, f'Added modules `{arguments}` to `{message.channel.name}`')
                client.save_config()
            else:
                await client.send_message(message.channel,
                                          f'No module named `{arguments}` or already added to channel')
        else:
            warning = await client.send_message(message.channel, f'{message.author.mention} is not in the sudoers '
                                                                 f'file. This incident will be reported.')
            await asyncio.sleep(60)
            await client.delete_message(warning)

    async def channel_list(self, client: discord.Client, message: discord.Message, arguments: str):
        if message.channel.permissions_for(message.author).administrator:
            message_string = '```\nAvailable modules:'

            for module in client.modules:
                message_string += '\n\t' + module.name

            message_string += "```"

            await client.send_message(message.channel, message_string)

        else:
            warning = await client.send_message(message.channel, f'{message.author.mention} is not in the sudoers '
                                                                 f'file. This incident will be reported.')
            await asyncio.sleep(60)
            await client.delete_message(warning)
