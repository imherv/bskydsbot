# BOT DESENVOLVIDO POR:
# HERV | HERV DESIGN
# @hervdesign.com (BlueSky)
# @imherv (Discord)

import discord
from discord.ext import commands
import requests
import pytz
import datetime
import asyncio
import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading

# Configurações do bot
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
BLUESKY_API_URL = os.environ['BLUESKY_API_URL']
channel_id = int(os.environ['channel_id'])

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

last_post_id = None
timezone = pytz.timezone('America/Sao_Paulo')

def fetch_bluesky_posts():
    try:
        response = requests.get(BLUESKY_API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro na API Bluesky: {response.status_code}")
            return None
    except Exception as e:
        print(f"Erro ao acessar Bluesky API: {e}")
        return None

def convert_at_to_https(post_url):
    if post_url.startswith('at://'):
        # Converte o link at:// para https://bsky.app/profile/...
        post_url = post_url.replace('at://did:plc:', 'https://bsky.app/profile/did:plc:')
        post_url = post_url.replace('/app.bsky.feed.post/', '/post/')
    return post_url

async def send_new_post(channel, post):
    post_content = post.get('post', {}).get('record', {}).get('text', "Post sem conteúdo disponível")
    author = post.get('post', {}).get('author', {})
    author_handle = author.get('handle', 'desconhecido')
    author_avatar = author.get('avatar', '')  # URL da foto de perfil
    post_url = post.get('post', {}).get('uri', '')

    post_url = convert_at_to_https(post_url)  # Converte o URL do post, se necessário

    embed = discord.Embed(
        description=post_content,
        color=0xff0053  # Cor do embed em hexadecimal
    )
    
    # Adiciona o ícone do Bluesky ao lado do nome do autor
    bluesky_icon = "https://bsky.app/static/favicon-16x16.png"
    embed.set_author(name=f"@{author_handle}", icon_url=bluesky_icon)
    
    # Adiciona a imagem ao embed se disponível
    embed_data = post.get('post', {}).get('embed', {})
    if embed_data and embed_data.get('$type') == 'app.bsky.embed.images#view':
        images = embed_data.get('images', [])
        if images:
            fullsize_image_url = images[0].get('fullsize', '')
            if fullsize_image_url.startswith(('http://', 'https://')):
                embed.set_image(url=fullsize_image_url)

    # Adiciona o ícone do autor como thumbnail ao lado da embed
    if author_avatar.startswith(('http://', 'https://')):
        embed.set_thumbnail(url=author_avatar)


    # Adiciona o link completo na descrição do embed
    embed.description += f"\n\n[Visualizar no BlueSky]({post_url})"

    try:
        message = await channel.send(embed=embed)
        print(f"Mensagem enviada: {post_url}")
        
        # Adiciona uma reação de coração vermelho na mensagem enviada
        await message.add_reaction("❤️")
    except discord.DiscordException as e:
        print(f"Erro ao enviar mensagem: {e}")

# Variável global para armazenar o timestamp da última postagem
last_post_timestamp = None

async def check_new_posts():
    global last_post_timestamp
    await bot.wait_until_ready()
    
    channel = bot.get_channel(channel_id)

    if channel is None:
        print("Canal não encontrado. Verifique o ID do canal.")
        return

    while not bot.is_closed():
        posts_data = fetch_bluesky_posts()
        if posts_data and 'feed' in posts_data:
            for post_item in posts_data['feed']:
                post_data = post_item.get('post', {})
                root = post_item.get('reply', {}).get('root', None)  # Verifica se há um root associado

                if root is None:  # Apenas processa se não houver root (postagem normal)
                    post_id = post_data.get('uri', '')
                    post_timestamp = post_data.get('indexedAt', '')
                    
                    # Converte o timestamp da postagem para datetime
                    try:
                        post_time = datetime.datetime.fromisoformat(post_timestamp.replace('Z', '+00:00'))
                    except ValueError:
                        continue

                    # Verifica se a postagem é nova e ocorre após o último timestamp registrado
                    if (last_post_timestamp is None) or (post_time > last_post_timestamp):
                        last_post_timestamp = post_time  # Atualiza o timestamp da última postagem processada
                        await send_new_post(channel, post_item)
        
        await asyncio.sleep(2)  # Verifica novos posts a cada 3 segundos.

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    bot.loop.create_task(check_new_posts())

@bot.command(name="limpar", help="Apaga todas as mensagens enviadas pelo bot.")
@commands.has_permissions(administrator=True)
async def clear(ctx):
    if ctx.author.guild_permissions.administrator:
        channel = ctx.channel
        def is_bot_msg(msg):
            return msg.author == bot.user
        deleted = await channel.purge(limit=100, check=is_bot_msg, bulk=True)
        await ctx.send(f"Todas as mensagens do bot foram apagadas! ({len(deleted)} mensagens deletadas)")
    else:
        await ctx.send("Você não tem permissão para usar este comando.")

# Função para iniciar um servidor HTTP simples
def run_http_server():
    port = 8000
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Servidor HTTP rodando na porta {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    # Executa o bot do Discord em paralelo ao servidor HTTP
    bot_thread = threading.Thread(target=bot.run, args=(DISCORD_TOKEN,))
    bot_thread.start()

    run_http_server()
    
# BOT DESENVOLVIDO POR:
# HERV | HERV DESIGN
# @hervdesign.com (BlueSky)
# @imherv (Discord)
