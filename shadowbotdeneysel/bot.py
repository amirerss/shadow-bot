import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# .env dosyasındaki verileri yükler
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# --- BOT AYARLARI VE İZİNLER ---
intents = discord.Intents.default()
intents.message_content = True # Botun mesajların içini (fotoğraf, video, metin) okumasını sağlar

bot = commands.Bot(command_prefix='!', intents=intents)

# Bot başlarken Cogs klasöründeki dosyaları otomatik yükler
@bot.event
async def setup_hook():
    print("Modüller yükleniyor...")
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"Yüklendi: {filename}")

    # Tüm slash komutlarını Discord'a senkronize et
    await bot.tree.sync()
    print("Tüm modüller ve Slash komutları başarıyla senkronize edildi!")

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yapıldı! Shadow Bot aktif.')

# Botu çalıştır
if TOKEN is None:
    print("HATA: .env dosyasında DISCORD_BOT_TOKEN bulunamadı! Lütfen dosyanızı kontrol edin.")
else:
    print("Bot başlatılıyor, lütfen bekleyin...")
    bot.run(TOKEN)