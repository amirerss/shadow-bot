import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
import os

YETKILI_ROLLER = [1483443654772396093 , 1494377287666368602 , 1494377031432147055 ]

# --- MERKEZİ KURULUM MENÜSÜ ---
class KurulumMenusu(View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot

    @discord.ui.button(label="🎫 Ticket Paneli", style=discord.ButtonStyle.primary, custom_id="kur_ticket")
    async def btn_ticket(self, interaction: discord.Interaction, button: Button):
        try:
            from cogs.ticket_modul import TicketPanel
            ticket_cog = self.bot.get_cog("TicketCog")
            if not ticket_cog:
                return await interaction.response.send_message("❌ Ticket modülü bulunamadı.", ephemeral=True)
            embed = discord.Embed(title="Destek", description="Destek talebi oluşturmak için aşağıdaki butona tıklayın.", color=0x2b2d31)
            embed.set_footer(text="Shadow Bot - Destek Sistemi")
            await interaction.channel.send(embed=embed, view=TicketPanel(ticket_cog))
            await interaction.response.send_message("✅ Ticket paneli bu kanala başarıyla kuruldu.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Hata oluştu: {e}", ephemeral=True)

    @discord.ui.button(label="ℹ️ Bilgi Paneli", style=discord.ButtonStyle.secondary, custom_id="kur_bilgi")
    async def btn_bilgi(self, interaction: discord.Interaction, button: Button):
        try:
            from cogs.bilgilendirme_modul import BilgilendirmeView
            embed = discord.Embed(title="ℹ️ Bilgilendirme Merkezi", description="Aradığınız veya merak ettiğiniz bilgilere buradan ulaşabilirsiniz.\n\nAşağıdaki butonları kullanarak tesis departmanları hakkında detaylı bilgi alabilir, sık sorulan sorulara göz atabilir veya sunucunun hikayesini (lore) inceleyebilirsiniz.", color=0x2b2d31)
            embed.set_footer(text="Shadow Roleplay • Bilgi Paneli")
            dosya_yolu = os.path.join("textures", "bilgilendirme.png")
            if os.path.exists(dosya_yolu):
                dosya = discord.File(dosya_yolu, filename="bilgilendirme.png")
                embed.set_image(url="attachment://bilgilendirme.png")
                await interaction.channel.send(file=dosya, embed=embed, view=BilgilendirmeView())
            else:
                await interaction.channel.send(embed=embed, view=BilgilendirmeView())
            await interaction.response.send_message("✅ Bilgilendirme paneli bu kanala başarıyla kuruldu.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Hata oluştu: {e}", ephemeral=True)

    @discord.ui.button(label="📝 Formları Kur", style=discord.ButtonStyle.success, custom_id="kur_forum")
    async def btn_forum(self, interaction: discord.Interaction, button: Button):
        try:
            from cogs.forumlar import form_embed_olustur, get_forum_data, save_forum_data
            veri = get_forum_data()
            embed = form_embed_olustur(veri)
            gonderilen_mesaj = await interaction.channel.send(embed=embed)
            veri["kanal_id"] = interaction.channel.id
            veri["mesaj_id"] = gonderilen_mesaj.id
            save_forum_data(veri)
            await interaction.response.send_message("✅ Başvuru formları paneli bu kanala başarıyla kuruldu.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Hata oluştu: {e}", ephemeral=True)

    @discord.ui.button(label="📜 Kuralları Kur", style=discord.ButtonStyle.danger, custom_id="kur_kurallar")
    async def btn_kurallar(self, interaction: discord.Interaction, button: Button):
        try:
            from cogs.kurallar_modul import ust_embed_olustur, kural_embed_olustur
            dosyalar = []
            eksik_dosyalar = []
            for dosya_adi in ["banner.png", "topluluk.png", "oyun.png"]:
                yol = os.path.join("textures", dosya_adi)
                if os.path.exists(yol):
                    dosyalar.append(discord.File(yol, filename=dosya_adi))
                else:
                    eksik_dosyalar.append(dosya_adi)
            if eksik_dosyalar:
                return await interaction.response.send_message(f"❌ Hata: `textures/` klasöründe şu dosyalar eksik: {', '.join(eksik_dosyalar)}", ephemeral=True)
            embed1 = ust_embed_olustur()
            embed2 = kural_embed_olustur("topluluk")
            embed3 = kural_embed_olustur("oyun")
            dosya_banner = discord.File(os.path.join("textures", "banner.png"), filename="banner.png")
            dosya_topluluk = discord.File(os.path.join("textures", "oyun.png"), filename="oyun.png")
            await interaction.channel.send(files=[dosya_banner, dosya_topluluk], embeds=[embed1, embed2])
            dosya_oyun = discord.File(os.path.join("textures", "topluluk.png"), filename="topluluk.png")
            await interaction.channel.send(file=dosya_oyun, embed=embed3)
            await interaction.response.send_message("✅ Kurallar paneli bu kanala başarıyla kuruldu.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Hata oluştu: {e}", ephemeral=True)

    @discord.ui.button(label="📋 Yetkili Tablosu", style=discord.ButtonStyle.secondary, custom_id="kur_yetkili")
    async def btn_yetkili(self, interaction: discord.Interaction, button: Button):
        try:
            from cogs.yetkili_ekip_modul import yetkili_embed_olustur, get_yetkili_data, save_yetkili_data
            veri = get_yetkili_data()
            embed = yetkili_embed_olustur(veri)
            gonderilen_mesaj = await interaction.channel.send(embed=embed)
            veri["kanal_id"] = interaction.channel.id
            veri["mesaj_id"] = gonderilen_mesaj.id
            save_yetkili_data(veri)
            await interaction.response.send_message("✅ Yetkili ekip tablosu bu kanala başarıyla kuruldu.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Hata oluştu: {e}", ephemeral=True)

    @discord.ui.button(label="💻 Geliştirici Tablosu", style=discord.ButtonStyle.secondary, custom_id="kur_gelistirici")
    async def btn_gelistirici(self, interaction: discord.Interaction, button: Button):
        try:
            from cogs.gelistirici_ekip_modul import gelistirici_embed_olustur, get_gelistirici_data, save_gelistirici_data
            veri = get_gelistirici_data()
            embed = gelistirici_embed_olustur(veri)
            gonderilen_mesaj = await interaction.channel.send(embed=embed)
            veri["kanal_id"] = interaction.channel.id
            veri["mesaj_id"] = gonderilen_mesaj.id
            save_gelistirici_data(veri)
            await interaction.response.send_message("✅ Geliştirici tablosu bu kanala başarıyla kuruldu.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Hata oluştu: {e}", ephemeral=True)

# --- COG TANIMLAMASI ---
class KurulumCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="kurulum", description="Tüm modüllerin tek bir noktadan kurulmasını sağlayan merkezi menü.")
    async def ana_kurulum(self, interaction: discord.Interaction):
        kullanici_rolleri = [rol.id for rol in interaction.user.roles]
        if not any(rol in YETKILI_ROLLER for rol in kullanici_rolleri):
            return await interaction.response.send_message("❌ Bu komutu kullanmak için yetkiniz yok!", ephemeral=True)

        embed = discord.Embed(
            title="⚙️ Shadow Bot Kurulum Merkezi",
            description="Hangi sistemi **şu an bulunduğun kanala** kurmak istiyorsan aşağıdaki butonlardan seçebilirsin.\n\n*⚠️ Not: Kurulum butonlarına basmadan önce sistemin kurulmasını istediğin doğru kanalda olduğundan emin ol.*",
            color=0x2b2d31
        )
        embed.set_footer(text="Shadow Roleplay • Kurulum Menüsü")

        await interaction.response.send_message(embed=embed, view=KurulumMenusu(self.bot), ephemeral=True)

async def setup(bot):
    await bot.add_cog(KurulumCog(bot))
