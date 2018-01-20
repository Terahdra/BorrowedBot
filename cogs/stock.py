import discord
from discord.ext import commands
from .utils.dataIO import dataIO
from bs4 import BeautifulSoup
from pushbullet import PushBullet
import requests
import datetime

class Stock:
    """Stock commands using Google Finance and PushBullet."""

    def __init__(self, bot):
        self.bot = bot
        self.profiles = dataIO.load_json("data/stock/profiles.json")

    def get_quote(symbol):
        base_url = 'http://finance.google.com/finance?q='
        html = requests.get(base_url + symbol).text
        soup = BeautifulSoup(html, "html.parser")
        quote = soup.find('span', attrs={'class': 'pr'}).text
        return quote

    @commands.command(pass_context=True, name="quote")
    async def stock(self, ctx, symbol):
        """Gets the quote of a stock, provided a symbol"""
        if symbol:
            symbol = symbol.upper()
        else:
            await self.bot.send_cmd_help(ctx)
            return
        date = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        quote = Stock.get_quote(symbol).strip('\n')
        msg = "The current quote for **{}** is: **{} USD** as of `{} UTC`".format(symbol, quote, date)
        await self.bot.say(msg)

    @commmands.group(name="pushbullet", no_pm=True, pass_context=True")
    async def _pushbullet(self, ctx):
        """PushBullet app utilized to send mobile notifications of stocks

        More information can be found on the guide:
        https://github.com/evanq123/MooBot."""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @_pushbullet.command(pass_context=True, name="add")
    async def add(self, ctx, key, symbol, threshold):
        """Adds a stock to a profile to keep track of

        Usage: `[p]pushbullet add api_key symbol threshold`"""
        if key not in self.profiles:

        dataIO.save_json("data/stock/profiles.json", self.profiles)

    @_pushbullet.command(pass_context=True, name="delete")
    async def delete(self, ctx, key):
        """Deletes a saved profile

        Usage: `[p]pushbullet delete api_key`"""


def check_folders():
    folders = ("data", "data/stock/")
    for folder in folders:
        if not os.path.exists(folder):
            print("Creating " + folder + " folder...")
            os.makedirs(folder)


def check_files():
    files = {
        "profiles.json"       : {},
    }

    for filename, value in files.items():
        if not os.path.isfile("data/stock/{}".format(filename)):
            print("Creating empty {}".format(filename))
            dataIO.save_json("data/stock/{}".format(filename), value)


def setup(bot):
    bot.add_cog(Stock(bot))
