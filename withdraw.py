import discord
from discord.ext import commands

class select(discord.ui.Select):
    def __init__(self,id):
        x = list(database.mydb['coins'].find())
        options = [discord.SelectOption(label=f'{i['name']} {i['symbol']}', value=f'{i['name']}') for i in x]
        super().__init__(placeholder='Select a coin:', min_values=1, max_values=1, options=options,custom_id="select:1")
    async def callback(self, interaction: discord.Interaction):
        x = database.mydb['users'].find_one({'discord_id':interaction.user.id})
        print(x)
        y = database.mydb['coins'].find_one({'name':self.values[0]})
        print(y)
        embed = discord.Embed()
        embed.title= f'{y['name']} {y['symbol']}'
        embed.description = f"Wallet Address: dbfkweuhowncwnckxncow88rp298ehde"
        print(embed)
        if interaction.message.flags.value == 64:
            await interaction.response.defer()
            await interaction.edit_original_response(embed=embed,view=Menu(interaction.user.id),content=None)
        else:
            await interaction.response.send_message(embed=embed,view=Menu(interaction.user.id),ephemeral=True)
class History_select(discord.ui.Select):
    def __init__(self,id):
        x = list(database.mydb['coins'].find())
        options = [discord.SelectOption(label=f'{i['name']} ({i['symbol']})', value=f'{i['name']}') for i in x]
        super().__init__(placeholder='Select a coin:', min_values=1, max_values=1, options=options,custom_id="select:2")
    async def callback(self, interaction: discord.Interaction):
        x = database.mydb['users'].find_one({'discord_id':interaction.user.id})
        print(x)
        y = database.mydb['coins'].find_one({'name':self.values[0]})
        print(y)
        embed = discord.Embed()
        embed.title= f'{y['name']} ({y['symbol']})'
        embed.description = f"{x['withdraw'][self.values[0]]['withdraw_history'] if self.values[0] in list(dict.keys(x['withdraw'])) else "You don't have any withdraw history!"}"
        print(embed)
        if interaction.message.flags.value == 64:
            await interaction.response.defer()
            await interaction.edit_original_response(embed=embed,view=History(interaction.user.id),content=None)
        else:
            await interaction.response.send_message(embed=embed,view=History(interaction.user.id),ephemeral=True)

class History(discord.ui.View):
    def __init__(self,id):
        super().__init__(timeout=None)
        self.add_item(History_select(id)) 


class Menu(discord.ui.View):
    def __init__(self,id):
        super().__init__(timeout=None)
        self.add_item(select(id))

class Withdraw_Menu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='withdraw', style=discord.ButtonStyle.blurple, custom_id='withdraw:1')
    async def send_otp(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content=f"Select a coin to withdraw :",view=Menu(interaction.user.id),ephemeral=True)

    @discord.ui.button(label='Withdraw_history', style=discord.ButtonStyle.blurple, custom_id='withdraw:2')
    async def verify_otp(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content=f"Select a coin:",view=History(interaction.user.id),ephemeral=True)


class Deposit(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        global database
        database = bot
        bot.add_view(Withdraw_Menu())

    @commands.Cog.listener()
    async def on_ready(self):
        print("withdraw.py is ready")

        guild = self.bot.guilds[0]
        category = discord.utils.get(guild.categories, name = "my_account")
        channel = discord.utils.get(category.channels, name = "withdraw")

        if channel is None:
            x = await guild.create_text_channel("withdraw", category = category)
            channel = self.bot.get_channel(x.id)
            await channel.send(view=Withdraw_Menu())

async def setup(bot):
    await bot.add_cog(Withdraw(bot))

Footer
