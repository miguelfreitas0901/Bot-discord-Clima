import re
import unicodedata
import requests
import discord
import random
from discord.ext import commands
import config  

API_KEY = config.API_KEY
DISCORD_TOKEN = config.DISCORD_TOKEN

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def remover_acentos(texto: str) -> str:
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

def buscar_coords(cidade_input: str):
    """Descobre latitude e longitude da cidade pelo nome."""
    cidade = remover_acentos(cidade_input)
    if "," not in cidade:
        cidade = f"{cidade},BR"

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": cidade, "appid": API_KEY}
    resp = requests.get(url, params=params, timeout=10)
    dados = resp.json()
    if str(dados.get("cod")) != "200":
        return None
    return dados["coord"]["lat"], dados["coord"]["lon"], dados["name"], dados["sys"]["country"]

@bot.event
async def on_ready():
    print(f"✅ Bot online como {bot.user}")

@bot.command()
async def chuva(ctx, *, cidade: str):
    try:
        coords = buscar_coords(cidade)
        if not coords:
            await ctx.send(f"❌ Não encontrei `{cidade}`.")
            return

        lat, lon, nome, pais = coords

        # Endpoint /forecast (liberado na versão gratuita)
        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY,
            "units": "metric",
            "lang": "pt_br"
        }
        resp = requests.get(url, params=params, timeout=10)
        dados = resp.json()

        if "list" not in dados:
            await ctx.send("⚠️ Não consegui obter previsão agora.")
            return

        # Pega os 6 primeiros blocos de 3h (~18h)
        blocos = dados["list"][:6]
        texto = ""
        for b in blocos:
            dt_txt = b["dt_txt"].split(" ")[1]  # pega hora
            pop = b.get("pop", 0) * 100
            texto += f"⏰ {dt_txt} → {pop:.0f}% de chance de chuva\n"

        # frases aleatórias
        frases = [
            "☂️ Melhor levar guarda-chuva!",
            "😎 Parece que hoje dá pra sair tranquilo.",
            "🌧️ Tá com cara de chuva, se cuida!",
            "🌂 Se chover, já sabe... Netflix e cobertor!",
            "🤔 O tempo anda indeciso, melhor se preparar!"
        ]
        frase_escolhida = random.choice(frases)

        embed = discord.Embed(
            title=f"🌧️ Chance de chuva em {nome} ({pais})",
            description=texto + "\n\n" + frase_escolhida,
            color=discord.Color.blue()
        )
        embed.set_footer(text="Fonte: OpenWeather (próximas ~18h)")

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"⚠️ Erro: {type(e).__name__}: {e}")
        
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Esse comando não existe 😅")

@bot.command()
async def olá(ctx):
    await ctx.send(f"Olá! {ctx.author.name} 👋")


bot.run(DISCORD_TOKEN)