import discord
 
intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)
 
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
 
@client.event
async def on_message(message):
    print("message-->", message)
 
    if message.author == client.user:
        return
 
    if message.content.startswith('hola'):
        await message.channel.send('Hola!')
 
    if message.content.startswith('imagen'):
        await message.channel.send(file=discord.File('download.jpg'))
 
    if message.content.startswith('video'):
        await message.channel.send(file=discord.File('sample-mp4-file-small.mp4'))
 
    if message.content.startswith('audio'):
        await message.channel.send(file=discord.File('file_example_MP3_700KB.mp3'))
 
    if message.content.startswith('file'):
        await message.channel.send(file=discord.File('sample.pdf'))
 
client.run('<Your Bot Token>')