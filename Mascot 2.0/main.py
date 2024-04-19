import settings
import discord 
from discord.ext import commands
from schedule import get_upcoming_schedule

logger = settings.logging.getLogger("bot")

def run():
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"{bot.user} is Ready")
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")

    @bot.command(
            help="I am still under development!",
            description="Posting the schedule",
            brief="Posts the schedule",
            hidden=True
    )
    async def upc(ctx, day, month, date, team_num):
        """ Upcoming schedule to same channel: 
        FORMAT: !upc Thursday, July 5 """
        
        message = get_upcoming_schedule(day, month, date, team_num)

        await ctx.send(message)
        
    
    

    bot.run(settings.DISCORD_API_SECRET)
    #bot.run("") #for quick testing

if __name__ == '__main__':
    run()