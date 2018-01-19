import discord
from discord.ext import commands
from bs4 import BeautifulSoup
from pushbullet import PushBullet
import requests
import datetime

class Stock:
    """Stock commands using Google Finance and PushBullet."""

    def __init__(self, bot):
        self.bot = bot

    def _get_quote(symbol):
        base_url = 'http://finance.google.com/finance?q='
        html = requests.get(base_url + symbol).text
        soup = BeautifulSoup(html, "html.parser")
        quote = soup.find('span', attrs={'class': 'pr'}).text
        return quote

    @commands.command(pass_context=True, name="quote")
    async def stock(self, ctx, *, symbol):
        """Gets the quote of a stock, provided a symbol"""
        if symbol:
            symbol = symbol.upper()
        else:
            await self.bot.send_cmd_help(ctx)
            return
        date = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        quote = Stock._get_quote(symbol).rstrip()
        msg = "The current quote for **{}** is: **{} USD** as of `{} UTC`".format(symbol, quote, date)
        await self.bot.say(msg)

    @commmands.group(name="pushbullet", no_pm=True, pass_context=True")
    async def _pushbullet(self, ctx):
        """PushBullet app utilized to send mobile notifications of stocks

        More information can be found on the guide:
        https://github.com/evanq123/MooBot."""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @_pushbullet.command(pass_context=True, name="pushstock")
    async def add(self, ctx, *, symbol, threshold, key):
        """Adds a stock to keep track of.

        Usage: `[p]pushbullet add symbol threshold api_key`"""
        



def setup(bot):
    bot.add_cog(Stock(bot))
