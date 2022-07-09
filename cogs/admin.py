from __future__ import annotations

from typing import Literal, TYPE_CHECKING

import discord
from discord import app_commands, Interaction, ui
from discord.ext import commands

if TYPE_CHECKING:
    from bot import ValorantBot


class Admin(commands.Cog):
    """Error handler"""

    def __init__(self, bot: ValorantBot) -> None:
        self.bot: ValorantBot = bot

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context, sync_type: Literal['guild', 'global']) -> None:
        """ Sync the application commands """

        async with ctx.typing():
            if sync_type == 'guild':
                self.bot.tree.copy_global_to(guild=ctx.guild)
                await self.bot.tree.sync(guild=ctx.guild)
                await ctx.reply(f"Synced guild !")
                return

            await self.bot.tree.sync()
            await ctx.reply(f"Synced global !")

    @commands.command()
    @commands.is_owner()
    async def unsync(self, ctx: commands.Context, unsync_type: Literal['guild', 'global']) -> None:
        """ Unsync the application commands """

        async with ctx.typing():
            if unsync_type == 'guild':
                self.bot.tree.clear_commands(guild=ctx.guild)
                await self.bot.tree.sync(guild=ctx.guild)
                await ctx.reply(f"Un-Synced guild !")
                return

            self.bot.tree.clear_commands()
            await self.bot.tree.sync()
            await ctx.reply(f"Un-Synced global !")

    @app_commands.command(description='Shows basic information about the bot.')
    async def about(self, interaction: Interaction) -> None:
        """ Shows basic information about the bot. """

        owner_url = f'https://discord.com/users/240059262297047041'
        github_project = 'https://github.com/staciax/Valorant-DiscordBot'
        support_url = 'https://discord.gg/FJSXPqQZgz'

        embed = discord.Embed(color=0xffffff)
        embed.set_author(name='VALORANT STATS')
        embed.add_field(
            name='DEV:',
            value=f"D33P <$#0069",
            inline=False
        )
        embed.add_field(
            name='Info:',
            value=f"This bot is an external plugin of Vibez Discord Bot, and is still under development but still its fully usable.",
            inline=False
        )
        view = ui.View()
        view.add_item(ui.Button(label='SUPPORT', url='https://discord.gg/aquatic', row=0))
        view.add_item(ui.Button(label='INVITE VIBEZ', url='https://discord.com/oauth2/authorize?client_id=986286054409637958&permissions=140126841160&scope=bot%20applications.commands', row=0))

        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot: ValorantBot) -> None:
    await bot.add_cog(Admin(bot))
