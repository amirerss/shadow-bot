import discord
from discord.ext import commands
import json
import os

DATA_FILE = "bildirim_rolleri.json"

# Emoji ID -> Verilecek Rol ID Eşleştirmesi 
# (Sıfırları silip kendi Bildirim Rollerinin ID'lerini yapıştırmalısın)
REACTION_ROLES = {
    1551003852612829285: 111111111111111111, # SSU Bildirim Rolü ID
    1551003890944835600: 222222222222222222, # Güncelleme Bildirim Rolü ID
    1551003931683856454: 333333333333333333, # Sneak Peak Bildirim Rolü ID
    1551003963157909504: 444444444444444444, # Etkinlik Bildirim Rolü ID
    1551003990588923974: 555555555555555555  # Sosyal Medya Bildirim Rolü ID
}

def get_bildirim_data():
    if not os.path.exists(DATA_FILE):
        return {"kanal_id": None, "mesaj_id": None}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_bildirim_data(kanal_id, mesaj_id):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({"kanal_id": kanal_id, "mesaj_id": mesaj_id}, f, indent=4)

class BildirimRolleriCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Tepki tıklandığında rol verilir
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.member is None or payload.member.bot:
            return

        veri = get_bildirim_data()
        if payload.message_id != veri.get("mesaj_id"):
            return

        rol_id = REACTION_ROLES.get(payload.emoji.id)
        if rol_id:
            guild = self.bot.get_guild(payload.guild_id)
            rol = guild.get_role(rol_id)
            if rol:
                try:
                    await payload.member.add_roles(rol)
                except discord.Forbidden:
                    print(f"HATA: {rol.name} rolü verilemiyor. Botun rolü yeterince üstte değil.")
                except Exception as e:
                    print(f"Rol verilirken hata: {e}")

    # Tepki geri çekildiğinde rol alınır
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        veri = get_bildirim_data()
        if payload.message_id != veri.get("mesaj_id"):
            return

        rol_id = REACTION_ROLES.get(payload.emoji.id)
        if rol_id:
            guild = self.bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if member and not member.bot:
                rol = guild.get_role(rol_id)
                if rol:
                    try:
                        await member.remove_roles(rol)
                    except:
                        pass

async def setup(bot):
    await bot.add_cog(BildirimRolleriCog(bot))
