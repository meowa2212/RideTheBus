'''
Wojciech Gorzynski
04-06-2025 v1

an implementation of the "RideTheBus" game from a game called "Schedule 1"
into a discord bot
'''

import discord
from discord.ext import commands
from DiscordRTBgame import RideTheBus
from DiscordRTBbalance import Wallet

# Set up intents
intents = discord.Intents.default()
intents.message_content = True  # REQUIRED to receive message content in events

# Create the bot instance
bot = commands.Bot(command_prefix="!", intents=intents)
file_name = "DiscordRTBbalance_log.txt"
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You're missing a required argument for this command. Use '!helpme'")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid argument type. Make sure you're using the correct format. Use '!helpme'")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Unknown command. Use '!helpme'")
    else:
        await ctx.send(f"An unexpected error occurred")
        print(f"An unexpected error occurred: {str(error)}")

@bot.command()
async def helpme(ctx):
    print(f"{ctx.author} asked for help")
    embed = discord.Embed(
        title = "Ride The Bus List of commands",
        description = ''' !startgame <bet> -> starts the Ride The Bus game
        !balance -> shows your balance
        !ranking -> shows the players ranked on amount of money
        !help -> shows all the avaiable commands
        ''',
        color = discord.Color.light_grey()
    )
    await ctx.send(embed = embed)

@bot.command()
async def balance(ctx):
    print(f"{ctx.author} checked his balance")
    
    wallet = Wallet(ctx.author, file_name)
    embed = discord.Embed(
        title = "Balance",
        description = f"Your Balance is {wallet.get_balance()}$",
        color = discord.Color.dark_green()
    )
    await ctx.send_message(embed = embed)
    
@bot.command()
async def ranking(ctx):
    print(f"{ctx.author} checked the ranking")
    wallet = Wallet(ctx.author, file_name)
    accounts = wallet.ranking()
    description = "Richest players:\n"
    for account in accounts:
        description += f"{account[0]}: {account[1]}$\n"
        
    embed = discord.Embed(
        title = "Ranking",
        description = description,
        color = discord.Color.gold()
    )
    await ctx.send(embed = embed)

@bot.command()
async def startgame(ctx, bet: int = 100):
    if bet <= 0:
        await ctx.send("Bet must be a positive number.", )
        return
    if bet > 500:
        await ctx.send("Max bet is 500$")
        return
    
    print(f"{ctx.author} started the game")
    wallet = Wallet(ctx.author, file_name)
    wallet.set_balance(wallet.get_balance()-bet)
    game = RideTheBus(bet)
    
    embed = discord.Embed(
        title="Ride The Bus",
        description=f'''Welcome, {ctx.author}.
                        Your balance: {wallet.get_balance()}$, you bet {bet}$''',
        color=discord.Color.green()
    )
    view = ViewWelcome(embed, ctx.author, game, wallet)
    await ctx.send(embed=embed, view=view)

class View(discord.ui.View):
    def __init__(self, embed, user: discord.User, game: RideTheBus, wallet, timeout=180):
        super().__init__(timeout=timeout)
        self.wallet = wallet
        self.user = user
        self.game = game

    def lost_embed(self):
        return discord.Embed(
            title = "You Lost!",
            description = f'''Your balance is {self.wallet.get_balance()}$
                            used cards: {self.cards_used()}''',
            color = discord.Color.red()
        )

    def won_embed(self):
        return discord.Embed(
            title="You Won!",
            description=f'''You won this round, your bet is worth {self.game.bet*self.game.multiplier}$
                            new card: {self.game.string_card(self.game.cards_used[-1])}''',
            color=discord.Color.gold()
        )
    
    def won_final_embed(self):
        self.wallet.change_balance(self.game.bet*self.game.multiplier)
        return discord.Embed(
            title = "End of game, You Won!",
            description = f'''You won {self.game.bet*self.game.multiplier}$, you now have {self.wallet.get_balance()}$
                            new card: {self.game.string_card(self.game.cards_used[-1])}
                            cards used: {self.cards_used()}''',
            color = discord.Color.gold()
        )

    def cards_used(self):
        strings = ["\n"+self.game.string_card(card) for card in self.game.cards_used]
        return_str = ""
        for string in strings:
            return_str += string
        return return_str

    
class ViewWelcome(View):
    def __init__(self, embed, user, game, wallet, timeout=180):
        super().__init__(embed, user, game, wallet, timeout)

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
        print(self.game.last_card())
        new_view = ColorGame(color_embed, self.user, self.game, self.wallet)
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
            description=f'''Made by meowa2212 (Wojciech Gorzynski) on 01-06-2025,
                            an open source (hopefully accurate) copy of a "Ride The Bus" card game from Schedule 1.
                            link to original: https://store.steampowered.com/app/3164500/Schedule_I/
                            link to github profile: https://github.com/meowa2212''',
            color=discord.Color.blue()
        )
        await interaction.channel.send(embed=info_embed)
        await interaction.message.edit(view=self)

class ColorGame(View):
    def __init__(self, embed, user, game, wallet, timeout=180):
        super().__init__(embed, user, game, wallet, timeout)

    @discord.ui.button(label="Red", style=discord.ButtonStyle.danger)
    async def red_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("You can't use this button.", ephemeral=True)
            return

        if self.game.color("Red"):
            new_view = Continue(embed = self.won_embed(), user = self.user, game = self.game, wallet = self.wallet)
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
            new_view = Continue(embed = self.won_embed(), user = self.user, game = self.game, wallet = self.wallet)
            await interaction.channel.send(embed = self.won_embed(), view = new_view)
        else:
            await interaction.channel.send(embed = self.lost_embed())

        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        await interaction.response.edit_message(view = self)

class HighLowGame(View):
    def __init__(self, embed, user, game, wallet, timeout = 180):
        super().__init__(embed, user, game, wallet, timeout) 
        
    @discord.ui.button(label = "Higher", style = discord.ButtonStyle.danger)
    async def high_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("You can't use this button.", ephemeral=True)
            return

        if self.game.high_low("High"):
            new_view = Continue(embed = self.won_embed(), user = self.user, game = self.game, wallet = self.wallet)
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
            new_view = Continue(embed = self.won_embed(), user = self.user, game = self.game, wallet = self.wallet)
            await interaction.channel.send(embed = self.won_embed(), view = new_view)
        else:
            await interaction.channel.send(embed = self.lost_embed())

        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        await interaction.response.edit_message(view = self) 

class InOutGame(View):
    def __init__(self, embed, user, game, wallet, timeout = 180):
        super().__init__(embed, user, game, wallet, timeout) 
        
    @discord.ui.button(label = "In", style = discord.ButtonStyle.danger)
    async def in_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("You can't use this button.", ephemeral=True)
            return

        if self.game.in_out("In"):
            new_view = Continue(embed = self.won_embed(), user = self.user, game = self.game, wallet = self.wallet)
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
            new_view = Continue(embed = self.won_embed(), user = self.user, game = self.game, wallet = self.wallet)
            await interaction.channel.send(embed = self.won_embed(), view = new_view)
        else:
            await interaction.channel.send(embed = self.lost_embed())

        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        await interaction.response.edit_message(view = self)     

class SuitGame(View):
    def __init__(self, embed, user, game, wallet, timeout = 180):
        super().__init__(embed, user, game, wallet, timeout) 
        
    @discord.ui.button(label = "Spades", style = discord.ButtonStyle.secondary, emoji = "♠️")
    async def spades_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("You can't use this button.", ephemeral=True)
            return

        if self.game.suit("S"):
            await interaction.channel.send(embed = self.won_final_embed())
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
            await interaction.channel.send(embed = self.won_final_embed())
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
            await interaction.channel.send(embed = self.won_final_embed())
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
            self.wallet.change_balance(self.game.bet*self.game.multiplier)
            await interaction.channel.send(embed = self.won_embed())
        else:
            await interaction.channel.send(embed = self.lost_embed())

        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        await interaction.response.edit_message(view = self)
               
class Continue(View):
    def __init__(self, embed, user, game, wallet, timeout=180):
        super().__init__(embed, user, game, wallet, timeout)

    @discord.ui.button(label="Continue", style=discord.ButtonStyle.primary)
    async def continue_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("You can't use this button.", ephemeral = True)
            return
            
        if self.game.in_out_passed:
            continue_embed = discord.Embed(
                title = "Suit Game!",
                description = f'''Choose the next card's suit.
                                multiplier = 20x
                                cards on the table: {self.cards_used()}''',
                color = discord.Color.blue()
            )
            print(self.game.last_card())
            new_view = SuitGame(embed = continue_embed, user = self.user, game = self.game, wallet = self.wallet)
            await interaction.channel.send(embed = continue_embed, view = new_view)
       
       
        elif self.game.high_low_passed:
            continue_embed = discord.Embed(
                title = "In and Out Game!",
                description = f'''Choose if the next card will be inside the previous two or on the outside.
                                multiplier = 4x
                                cards on the table: {self.cards_used()}''',
                color = discord.Color.blue()
            )
            print(self.game.last_card())
            new_view = InOutGame(embed = continue_embed, user = self.user, game = self.game, wallet = self.wallet)
            await interaction.channel.send(embed = continue_embed, view = new_view)
        
        
        elif self.game.color_passed:
            continue_embed = discord.Embed(
                title = "High Low Game!",
                description = f'''Choose if the next card will be of higher value or lower than the previous.
                                multiplier = 3x
                                cards on the table: {self.cards_used()}''',
                color = discord.Color.blue()
            )
            print(self.game.last_card())
            new_view = HighLowGame(embed = continue_embed, user = self.user, game = self.game, wallet = self.wallet)
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

        self.wallet.change_balance(self.game.bet*self.game.multiplier)
        
        quit_embed = discord.Embed(
            title = "End of Game",
            description = f"You paid out, you won {self.game.bet*self.game.multiplier}$, you now have {self.wallet.get_balance()}$",
            color = discord.Color.light_grey()
        )
        
        await interaction.channel.send(embed = quit_embed)

        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        await interaction.response.edit_message(view=self)

# Run the bot
bot.run("MTM3OTA4NTg4ODkyNzA0MzY5Ng.GzWTPZ.7VA2BFFzGRXczniOXETRDgZROdXmfyo30kycDM")