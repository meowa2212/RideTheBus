'''
Wojciech Gorzynski
02-06-2025 v1

an implementation of the "RideTheBus" game from a game called "Schedule 1"
into a discord bot
'''

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
        self.user = user
        self.game = game

    def lost_embed(self):
        return discord.Embed(
            title="You Lost!",
            description=f'''Your balance is {self.game.balance}
                            used cards: {self.game.cards_used}''',
            color=discord.Color.red()
        )

    def won_embed(self):
        return discord.Embed(
            title="You Won!",
            description=f'''You won this round, your bet is {self.game.bet*self.game.multiplier}
                            used cards: {self.game.cards_used}''',
            color=discord.Color.gold()
        )

class ViewWelcome(View):
    def __init__(self, embed, user, game, timeout=180):
        super().__init__(embed, user, game, timeout)

    @discord.ui.button(label="Start Game", style=discord.ButtonStyle.success, emoji="🎮")
    async def start_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("You can't use this button.", ephemeral=True)
            return

        color_embed = discord.Embed(
            title="Color Game!",
            description='''Choose if the next card will be Red or Black. 
                            multiplier = 2x''',
            color=discord.Color.blue()
        )
        new_view = ColorGame(color_embed, self.user, self.game)
        await interaction.channel.send(embed=color_embed, view=new_view)

        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        await interaction.response.edit_message(view = self)

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
            new_view = Continue(embed = self.won_embed(), user = self.user, game = self.game)
            await interaction.channel.send(embed = self.won_embed(), view = new_view)
        else:
            await interaction.channel.send(embed = self.lost_embed())

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
            new_view = Continue(embed = self.won_embed(), user = self.user, game = self.game)
            await interaction.channel.send(embed = self.won_embed(), view = new_view)
        else:
            await interaction.channel.send(embed = self.lost_embed())

        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        await interaction.response.edit_message(view = self)

class HighLowGame(View):
    def __init__(self, embed, user, game, timeout = 180):
        super().__init__(embed, user, game, timeout) 
        
    @discord.ui.button(label = "Higher", style = discord.ButtonStyle.danger)
    async def high_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("You can't use this button.", ephemeral=True)
            return

        if self.game.high_low("High"):
            new_view = Continue(embed = self.won_embed(), user = self.user, game = self.game)
            await interaction.channel.send(embed = self.won_embed(), view = new_view)
        else:
            await interaction.channel.send(embed = self.lost_embed())

        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        await interaction.response.edit_message(view = self)  
    
    @discord.ui.button(label="Lower", style=discord.ButtonStyle.secondary)
    async def low_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("You can't use this button.", ephemeral=True)
            return

        if self.game.high_low("Low"):
            new_view = Continue(embed = self.won_embed(), user = self.user, game = self.game)
            await interaction.channel.send(embed = self.won_embed(), view = new_view)
        else:
            await interaction.channel.send(embed = self.lost_embed())

        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        await interaction.response.edit_message(view = self) 

class InOutGame(View):
    def __init__(self, embed, user, game, timeout = 180):
        super().__init__(embed, user, game, timeout) 
        
    @discord.ui.button(label = "In", style = discord.ButtonStyle.danger)
    async def in_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("You can't use this button.", ephemeral=True)
            return

        if self.game.in_out("In"):
            new_view = Continue(embed = self.won_embed(), user = self.user, game = self.game)
            await interaction.channel.send(embed = self.won_embed(), view = new_view)
        else:
            await interaction.channel.send(embed = self.lost_embed())

        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        await interaction.response.edit_message(view = self)  
    
    @discord.ui.button(label="Out", style=discord.ButtonStyle.secondary)
    async def out_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("You can't use this button.", ephemeral=True)
            return

        if self.game.in_out("Out"):
            new_view = Continue(embed = self.won_embed(), user = self.user, game = self.game)
            await interaction.channel.send(embed = self.won_embed(), view = new_view)
        else:
            await interaction.channel.send(embed = self.lost_embed())

        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        await interaction.response.edit_message(view = self)     

class SuitGame(View):
    def __init__(self, embed, user, game, timeout = 180):
        super().__init__(embed, user, game, timeout) 
        
    @discord.ui.button(label = "Spades", style = discord.ButtonStyle.secondary, emoji = "♠️")
    async def spades_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("You can't use this button.", ephemeral=True)
            return

        if self.game.suit("S"):
            new_view = Continue(embed = self.won_embed(), user = self.user, game = self.game)
            await interaction.channel.send(embed = self.won_embed(), view = new_view)
        else:
            await interaction.channel.send(embed = self.lost_embed())

        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        await interaction.response.edit_message(view = self)
        
    @discord.ui.button(label = "Hearts", style = discord.ButtonStyle.danger, emoji = "♥️")
    async def hearts_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("You can't use this button.", ephemeral=True)
            return

        if self.game.suit("H"):
            new_view = Continue(embed = self.won_embed(), user = self.user, game = self.game)
            await interaction.channel.send(embed = self.won_embed(), view = new_view)
        else:
            await interaction.channel.send(embed = self.lost_embed())

        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        await interaction.response.edit_message(view = self) 
        
    @discord.ui.button(label = "Clubs", style = discord.ButtonStyle.secondary, emoji = "♣️")
    async def clubs_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("You can't use this button.", ephemeral=True)
            return

        if self.game.suit("C"):
            new_view = Continue(embed = self.won_embed(), user = self.user, game = self.game)
            await interaction.channel.send(embed = self.won_embed(), view = new_view)
        else:
            await interaction.channel.send(embed = self.lost_embed())

        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        await interaction.response.edit_message(view = self)

    @discord.ui.button(label = "Diamonds", style = discord.ButtonStyle.danger, emoji = "♦️")
    async def diamonds_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("You can't use this button.", ephemeral=True)
            return

        if self.game.suit("D"):
            new_view = Continue(embed = self.won_embed(), user = self.user, game = self.game)
            await interaction.channel.send(embed = self.won_embed(), view = new_view)
        else:
            await interaction.channel.send(embed = self.lost_embed())

        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        await interaction.response.edit_message(view = self)
    

               
class Continue(View):
    def __init__(self, embed, user, game, timeout=180):
        super().__init__(embed, user, game, timeout)

    @discord.ui.button(label="Continue", style=discord.ButtonStyle.primary)
    async def continue_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("You can't use this button.", ephemeral = True)
            return

        if self.game.suit_passed:
            self.game.balance += self.game.bet*self.game.multiplier
            continue_embed = discord.Embed(
                title = "End of game, You Won!",
                description = f'''You won {self.game.bet}, you now have {self.game.balance}
                                cards used {self.game.cards_used}''',
                color = discord.Color.gold()
            )
            await interaction.channel.send(embed = continue_embed)
            
        
        elif self.game.in_out_passed:
            continue_embed = discord.Embed(
                title = "Suit Game!",
                description = '''Choose the next card's suit.
                                multiplier = 20x''',
                color = discord.Color.blue()
            )
            new_view = SuitGame(embed = continue_embed, user = self.user, game = self.game)
            await interaction.channel.send(embed = continue_embed, view = new_view)
       
       
        elif self.game.high_low_passed:
            continue_embed = discord.Embed(
                title = "In and Out Game!",
                description = '''Choose if the next card will be inside the previous two or on the outside.
                                multiplier = 4x''',
                color = discord.Color.blue()
            )
            new_view = InOutGame(embed = continue_embed, user = self.user, game = self.game)
            await interaction.channel.send(embed = continue_embed, view = new_view)
        
        
        elif self.game.color_passed:
            continue_embed = discord.Embed(
                title = "High Low Game!",
                description = '''Choose if the next card will be of higher value or lower than the previous.
                                multiplier = 3x''',
                color = discord.Color.blue()
            )
            new_view = HighLowGame(embed = continue_embed, user = self.user, game = self.game)
            await interaction.channel.send(embed = continue_embed, view = new_view)          



        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Payout", style=discord.ButtonStyle.secondary)
    async def payout_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("You can't use this button.", ephemeral=True)
            return

        self.game.balance += self.game.bet*self.game.multiplier
        
        quit_embed = discord.Embed(
            title = "End of Game",
            description = f"You paid out, you won {self.game.bet}, you now have {self.game.balance}",
            color = discord.Color.light_grey()
        )
        
        await interaction.channel.send(embed = quit_embed)

        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        await interaction.response.edit_message(view=self)

# Run the bot
bot.run("bot token here")