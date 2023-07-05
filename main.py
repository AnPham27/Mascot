import settings
import discord 
from discord.ext import commands
import random
from datetime import date
from standings_scraper import standings
from schedule_scraper import get_schedule, get_upcoming_schedule



#filename = "schedule.txt"
logger = settings.logging.getLogger("bot")

def run():
    intents = discord.Intents.default()

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        #schedule.every().thursday.at("10:00").do(asyncio.run, send_weekly_message)


    @bot.command(
            help="I am still under development!",
            description="Ping pong?",
            brief="Ping pong!",
            hidden=True
    )


    async def ping(ctx):
        """ Answers with pong """
        await ctx.send("pong")

    @bot.command(
            help="I am still under development!",
            description="Posting the schedule",
            brief="Posts the schedule",
            hidden=True
    )

    async def schedule(ctx):
        """ Answers with the schedule for that day """
        await weekly_schedule(ctx)

    async def weekly_schedule(ctx):
        #channel = bot.get_channel(1112936855088943165)
        await ctx.send(get_schedule())
    


    @bot.command(
            help="I am still under development!",
            description="Posting the schedule",
            brief="Posts the schedule",
            hidden=True
    )
    async def upcoming_schedule(ctx, date1, date2, date3):
        """ Answers with the schedule for that day """
        day = f"{date1} {date2} {date3}"
        await next_schedule(ctx, day)

    async def next_schedule(ctx,day):
        # channel = bot.get_channel(1112936855088943165)
        message = get_upcoming_schedule(day)

        await ctx.send(message)


    @bot.command(
            help="I am still under development!",
            description="Posting the schedule",
            brief="Posts the schedule",
            hidden=True
    )
    async def upcoming(ctx, date1, date2, date3):
        """ @EVERYONE the schedule for the day and the standing """
        day = f"{date1} {date2} {date3}"
        await everyone_schedule(ctx, day)

    async def everyone_schedule(ctx, day):
        channel = bot.get_channel(1109852414972010586) #@ main channel
        #channel = bot.get_channel(1112936855088943165) #@ bot testing channel
        message = f"@everyone {get_upcoming_schedule(day)}"

        table, msg = standings()

        await channel.send(message)
        await channel.send(table)
        await channel.send(msg)

    @bot.command(
            help="I am still under development!",
            description="Posting the schedule",
            brief="Posts the schedule",
            hidden=True
    )
    async def standing(ctx):
        """ Answers with the standing for that day """
        await weekly_standing(ctx)
   

    async def weekly_standing(ctx):
        #channel = bot.get_channel(1112936855088943165)
        table, message = standings()
        await ctx.send(table)
        await ctx.send(message)

    # @bot.command(
    #         help="I am still under development!",
    #         description="Posting the playoffs",
    #         brief="Posts the playoffs",
    #         hidden=True
    # )
    # async def playoffs(ctx):
    #     """ Answers with the standing for that day """
    #     await playoff(ctx)
   
    # async def playoff(ctx):
    #     channel = bot.get_channel(1109852414972010586)

    #     #Thursday, June 22: our first game we are playing against DISCount Athletes wearing 
    #     # White on Margaret # 5. In our second game, we are playing against Deborah wearing White on Margaret # 4.

    #     msg = "@everyone Thursday, June 29: our first game we are playing against **Huck Tales** wearing **White** on **Margaret # 6**. In our second game, we are playing against **5 Alive** wearing **Dark** on **Margaret # 7**."
    #     table, message = standings()

    #     await channel.send(msg)
    #     await channel.send(table)
    #     await channel.send(message)

    bot.run(settings.DISCORD_API_SECRET)
    #bot.run("") #for quick testing




if __name__ == '__main__':
    run()