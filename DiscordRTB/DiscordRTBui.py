'''
Wojciech Gorzynski
02-06-2025 v1

an implementation of the "RideTheBus" game from a game called "Schedule 1"
into a discord bot
'''

# Replace this with your bot token
TOKEN = "MTM3OTA4NTg4ODkyNzA0MzY5Ng.GQSGf5.GPeZHttZt8RUaSMohuHbkTph5fre0dHc8KHYU4"

import discord
from discord.ext import commands
from DiscordRTBgame import RideTheBus

# Set up intents
intents = discord.Intents.default()
intents.message_content = True  # REQUIRED to receive message content in events

# Create the bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")

@bot.command()
async def startgame(ctx):
    embed = discord.Embed(
        title="Ride The Bus",
        description="Made by Meowa2212! Ride The Bus from schedule 1",
        color=discord.Color.green()
    )
    game = RideTheBus(0, 100)
    view = ViewWelcome(embed, ctx.author, game)
    await ctx.send(embed=embed, view=view)

class View(discord.ui.View):
    def __init__(self, embed: discord.Embed, user: discord.User, game: RideTheBus, timeout=180):
        super().__init__(timeout=timeout)
        self.welcome_embed = embed
        self.stored_embed = embed
        self.user = user
        self.game = game

        self.lost_screen = discord.Embed(
            title="You Lost!",
            description='''Your bet is gone!
                            Try again.
            ''',
            color=discord.Color.red()
        )

        self.continue_screen = discord.Embed(
            title="Do you want to continue?",
            color=discord.Color.blue()
        )

class ViewWelcome(View):
    def __init__(self, embed, user, game, timeout=180):
        super().__init__(embed, user, game, timeout)

    @discord.ui.button(label="Start Game", style=discord.ButtonStyle.success, emoji="🎮")
    async def clone_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("You can't use this button.", ephemeral=True)
            return

        self.stored_embed = discord.Embed(
            title="Color Game!",
            description='''Choose if the next card will be Red or Black! 
                            multiplier = 2x''',
            color=discord.Color.green()
        )
        new_view = ColorGame(self.stored_embed, self.user, self.game)
        await interaction.channel.send(embed=self.stored_embed, view=new_view)

        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Info", style=discord.ButtonStyle.primary, emoji="ℹ️")
    async def info_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("You can't use this button.", ephemeral=True)
            return

        await interaction.response.defer()

        info_embed = discord.Embed(
            title="Game Info",
            description=f'''Here’s some detailed info about the game.
                            {self.game.balance} {self.game.bet} {self.game.cards_used}''',
            color=discord.Color.blue()
        )
        await interaction.channel.send(embed=info_embed)
        await interaction.message.edit(view=self)

class ColorGame(View):
    def __init__(self, embed, user, game, timeout=180):
        super().__init__(embed, user, game, timeout)

    @discord.ui.button(label="Red", style=discord.ButtonStyle.danger)
    async def red_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("You can't use this button.", ephemeral=True)
            return

        if self.game.color("Red"):
            self.game.bet *= 2
            new_view = ViewWelcome(self.welcome_embed, self.user, self.game)
            await interaction.channel.send(embed=self.welcome_embed, view=new_view)
        else:
            self.game.bet = 100
            new_view = ViewWelcome(self.lost_screen, self.user, self.game)
            await interaction.channel.send(embed=self.lost_screen, view=new_view)

        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Black", style=discord.ButtonStyle.secondary)
    async def black_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("You can't use this button.", ephemeral=True)
            return

        if self.game.color("Black"):
            self.game.bet *= 2
            new_view = ViewWelcome(self.welcome_embed, self.user, self.game)
            await interaction.channel.send(embed=self.welcome_embed, view=new_view)
        else:
            self.game.bet = 100
            new_view = ViewWelcome(self.lost_screen, self.user, self.game)
            await interaction.channel.send(embed=self.lost_screen, view=new_view)

        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        await interaction.response.edit_message(view=self)
    


# Run the bot
bot.run(TOKEN)