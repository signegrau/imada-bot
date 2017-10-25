import asyncio

from module import Module


class ModuleManager(Module):
    def __init__(self):
        super(ModuleManager, self).__init__('modulemanager', [], {
            'channeladd': self.channel_add
        })

        self.admin_only = True

    async def channel_add(self, client, message, arguments):
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
