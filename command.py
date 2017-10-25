from typing import Callable, Any

import discord

CommandHandler = Callable[[discord.Client, discord.Message, str], Any]


class Command:
    def __init__(self, name: str, help: str, handler: CommandHandler):
        self.name = name
        self.help = help
        self.handler = handler

    def get_name(self) -> str:
        return self.name

    def get_help(self) -> str:
        return self.help

    def handle(self, client: discord.Client, message: discord.Message, argument: str):
        self.handler(client, message, argument)
