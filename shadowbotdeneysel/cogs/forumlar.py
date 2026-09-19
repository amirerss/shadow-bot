import discord
from discord.ext import commands
from discord import app_commands
import json
import os

YETKILI_ROLLER = [1545845833826697296, 1547908920964681729, 1545844425882865766]

# Özel Emojiler[cite: 9, 12]
TIK_EMOJILERI = {
    "Admin": "<:tik1:1548486735019909140>",
    "Gamemaster": "<:tik2:1548486772109877269>",
    "Geliştirici": "<:tik3:1548486837859782766>",
    "Aktör": "<:tik4:1548486872710250586>",
    "Etkinlik Sorumlusu": "✅" # Klasik tik eklendi
}
CARPI_EMOJI = "<:carpi:1548486925881581588>"

# --- JSON VERİTABANI YÖNETİMİ ---
def get_forum_data():
    dosya_adi = "forum_data.json"
    if not os.path.exists(dosya_adi):
        varsayilan_veri = {
            "kanal_id": None,
            "mesaj_id": None,
            "formlar": {
                "Gamemaster": {"durum": "Aktif", "link": "https://link_ekle.com"},
                "Admin": {"durum": "Aktif", "link": "https://link_ekle.com"},
                "Aktör": {"durum": "Aktif", "link": "https://link_ekle.com"},
                "Geliştirici": {"durum": "Aktif", "link": "https://link_ekle.com"},
                "Etkinlik Sorumlusu": {"durum": "Aktif", "link": "https://link_ekle.com"} # Yeni bölüm eklendi
            }
        }
        with open(dosya_adi, "w", encoding="utf-8") as f:
            json.dump(varsayilan_veri, f, indent=4, ensure_ascii=False)
        return varsayilan_veri

    with open(dosya_adi, "r", encoding="utf-8") as f:
        return json.load(f)

def save_forum_data(veri):
    with open("forum_data.json", "w", encoding="utf-8") as f:
        json.dump(veri, f, indent=4, ensure_ascii=False)

# --- GÖMÜLÜ MESAJ (EMBED) OLUŞTURUCU ---
def form_embed_olustur(veri):
    embed = discord.Embed(
        title="Bize Katılın!",
        color=0x2b2d31
    )

    metin = ""
    for rol, ayarlar in veri["formlar"].items():
        is_aktif = ayarlar["durum"].lower() == "aktif"

        # Aktifse role özel tik emojisi, inaktifse çarpı emojisi atanır[cite: 9, 12]
        durum_emoji = TIK_EMOJILERI.get(rol, "✅") if is_aktif else CARPI_EMOJI
        durum_metni = f"Aktif {durum_emoji}" if is_aktif else f"İnaktif {durum_emoji}"

        link = ayarlar["link"]

        # Format: Aktif <emoji> | **Rol Alım Formu** <emoji> [tıklayın](link)[cite: 9, 12]
        metin += f"{durum_metni} | **{rol} Alım Formu** {durum_emoji} [tıklayın]({link})\n\n"

    embed.description = metin
    embed.set_footer(text="Shadow Roleplay • Başvuru Formları")
    return embed


class ForumlarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    forum_grup = app_commands.Group(name="forumlar", description="Alım formları yönetim sistemi")

    @forum_grup.command(name="durum", description="Formun durumunu Aktif veya İnaktif olarak değiştirir.")
    @app_commands.describe(
        forum="Hangi formun durumunu güncelleyeceksin?",
        yeni_durum="Formun yeni durumu ne olacak?"
    )
    @app_commands.choices(forum=[
        app_commands.Choice(name="Gamemaster", value="Gamemaster"),
        app_commands.Choice(name="Admin", value="Admin"),
        app_commands.Choice(name="Aktör", value="Aktör"),
        app_commands.Choice(name="Geliştirici", value="Geliştirici"),
        app_commands.Choice(name="Etkinlik Sorumlusu", value="Etkinlik Sorumlusu") # Menüye eklendi
    ], yeni_durum=[
        app_commands.Choice(name="Aktif", value="Aktif"),
        app_commands.Choice(name="İnaktif", value="İnaktif")
    ])
    async def durum_guncelle(self, interaction: discord.Interaction, forum: app_commands.Choice[str], yeni_durum: app_commands.Choice[str]):
        await self.mesaji_yenile(interaction, forum.value, "durum", yeni_durum.value)

    @forum_grup.command(name="link", description="Formun başvuru linkini değiştirir.")
    @app_commands.describe(
        forum="Hangi formun linkini güncelleyeceksin?",
        yeni_link="Yeni başvuru linkini yapıştırın."
    )
    @app_commands.choices(forum=[
        app_commands.Choice(name="Gamemaster", value="Gamemaster"),
        app_commands.Choice(name="Admin", value="Admin"),
        app_commands.Choice(name="Aktör", value="Aktör"),
        app_commands.Choice(name="Geliştirici", value="Geliştirici"),
        app_commands.Choice(name="Etkinlik Sorumlusu", value="Etkinlik Sorumlusu") # Menüye eklendi
    ])
    async def link_guncelle(self, interaction: discord.Interaction, forum: app_commands.Choice[str], yeni_link: str):
        if not (yeni_link.startswith("http://") or yeni_link.startswith("https://")):
            return await interaction.response.send_message("❌ Geçerli bir link girmelisin (http:// veya https:// ile başlamalı).", ephemeral=True)

        await self.mesaji_yenile(interaction, forum.value, "link", yeni_link)

    async def mesaji_yenile(self, interaction, forum_adi, ayar_turu, yeni_deger):
        kullanici_rolleri = [rol.id for rol in interaction.user.roles]
        if not any(rol in YETKILI_ROLLER for rol in kullanici_rolleri):
            return await interaction.response.send_message("❌ Yetkiniz yok!", ephemeral=True)

        veri = get_forum_data()

        if veri["mesaj_id"] is None or veri["kanal_id"] is None:
            return await interaction.response.send_message("❌ Önce merkezi `/kurulum` panelini kullanarak formu kurmalısın.", ephemeral=True)

        veri["formlar"][forum_adi][ayar_turu] = yeni_deger
        save_forum_data(veri)

        try:
            kanal = self.bot.get_channel(veri["kanal_id"])
            mesaj = await kanal.fetch_message(veri["mesaj_id"])

            yeni_embed = form_embed_olustur(veri)
            await mesaj.edit(embed=yeni_embed)

            await interaction.response.send_message(f"✅ **{forum_adi}** formunun **{ayar_turu}** ayarı başarıyla güncellendi.", ephemeral=True)
        except discord.NotFound:
            await interaction.response.send_message("❌ Hedef mesaj bulunamadı. Silinmiş olabilir, lütfen tekrar `/kurulum` paneli üzerinden kurulum yapın.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Mesaj güncellenirken beklenmeyen bir hata oluştu: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ForumlarCog(bot))
