import nextcord
from nextcord.ext import commands
import sqlite3

intents = nextcord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Connect to the database
conn = sqlite3.connect('prefixes.db')
c = conn.cursor()

# Create the table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS prefixes
             (server_id INTEGER PRIMARY KEY, prefix TEXT)''')
conn.commit()

# Function to load prefixes from the database
def load_prefixes():
    c.execute('SELECT * FROM prefixes')
    prefixes = {str(server_id): prefix for server_id, prefix in c.fetchall()}
    return prefixes

# Function to save prefixes to the database
def save_prefix(server_id, prefix):
    c.execute('INSERT OR REPLACE INTO prefixes (server_id, prefix) VALUES (?, ?)', (server_id, prefix))
    conn.commit()

# Load prefixes
prefixes = load_prefixes()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@commands.has_permissions(administrator=True)
@bot.command()
async def setprefix(ctx, new_prefix):
    server_id = ctx.guild.id
    prefixes[str(server_id)] = new_prefix
    save_prefix(server_id, new_prefix)
    await ctx.send(f'Prefix changed to `{new_prefix}`')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    server_id = str(message.guild.id)
    prefix = prefixes.get(server_id, '!')  # If no prefix is set, default to '!'

    if message.content.startswith(prefix):
        await bot.process_commands(message)

# Your bot token
bot.run('YOUR_BOT_TOKEN')
