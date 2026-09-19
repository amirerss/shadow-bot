import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
import os

YETKILI_ROLLER = [1483443654772396093, 1494377287666368602, 1494377031432147055]

# --- MERKEZİ KURULUM MENÜSÜ ---
class KurulumMenusu(View):
    def __init__(self, bot):
        super().__init__(timeout=300) # Menü 5 dakika aktif kalır
        self.bot = bot

    @discord.ui.button(label="🎫 Ticket Paneli Kur", style=discord.ButtonStyle.primary, custom_id="kur_ticket")
    async def btn_ticket(self, interaction: discord.Interaction, button: Button):
        try:
            from cogs.ticket_modul import TicketPanel
            ticket_cog = self.bot.get_cog("TicketCog")
            
            if not ticket_cog:
                return await interaction.response.send_message("❌ Ticket modülü bulunamadı, dosya adını kontrol edin.", ephemeral=True)

            embed = discord.Embed(
                title="Destek",
                description="Destek talebi oluşturmak için aşağıdaki butona tıklayın.",
                color=0x2b2d31
            )
            embed.set_footer(text="Shadow Bot - Destek Sistemi")
            
            await interaction.channel.send(embed=embed, view=TicketPanel(ticket_cog))
            await interaction.response.send_message("✅ Ticket paneli bu kanala başarıyla kuruldu.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Hata oluştu: {e}", ephemeral=True)

    @discord.ui.button(label="ℹ️ Bilgilendirme Paneli Kur", style=discord.ButtonStyle.secondary, custom_id="kur_bilgi")
    async def btn_bilgi(self, interaction: discord.Interaction, button: Button):
        try:
            from cogs.bilgilendirme_modul import BilgilendirmeView
            
            embed = discord.Embed(
                title="Bilgilendirme Merkezi",
                description=(
                    "Shadow Roleplay; kapsamlı bir RP deneyimi sunan; karakter gelişimi, entrika ve strateji odaklı bir RP sunucusudur. "
                    "Aşağıdaki butonları kullanarak;\n"
                    "- Detaylı bilgilendirme alabilir,\n"
                    "- Sık sorulan sorulara göz atabilir,\n"
                    "- Sunucunun hikayesini (lore) inceleyebilirsiniz."
                ),
                color=0x2b2d31
            )
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

    @discord.ui.button(label="📝 Başvuru Formları Kur", style=discord.ButtonStyle.success, custom_id="kur_forum")
    async def btn_forum(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True) 
        try:
            from cogs.forumlar_modul import forum_embedler_olustur, get_forum_data, save_forum_data
            import os
            
            veri = get_forum_data()
            embedler = forum_embedler_olustur(veri)
            
            dosya_yolu = os.path.join("textures", "forum.png")
            if os.path.exists(dosya_yolu):
                dosya = discord.File(dosya_yolu, filename="forum.png")
                gonderilen_mesaj = await interaction.channel.send(file=dosya, embeds=embedler)
            else:
                gonderilen_mesaj = await interaction.channel.send(embeds=embedler)
            
            veri["kanal_id"] = interaction.channel.id
            veri["mesaj_id"] = gonderilen_mesaj.id
            save_forum_data(veri)
            
            await interaction.followup.send("✅ Başvuru formları paneli bu kanala başarıyla kuruldu.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Hata oluştu: {e}", ephemeral=True)

    @discord.ui.button(label="📜 Kurallar Paneli Kur", style=discord.ButtonStyle.danger, custom_id="kur_kurallar")
    async def btn_kurallar(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
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
                return await interaction.followup.send(f"❌ Hata: `textures/` klasöründe şu dosyalar eksik: {', '.join(eksik_dosyalar)}", ephemeral=True)

            embed1 = ust_embed_olustur()
            embed2 = kural_embed_olustur("topluluk")
            embed3 = kural_embed_olustur("oyun")
            
            await interaction.followup.send("✅ Kurallar paneli kanala gönderiliyor...", ephemeral=True)

            dosya_banner = discord.File(os.path.join("textures", "banner.png"), filename="banner.png")
            dosya_topluluk = discord.File(os.path.join("textures", "oyun.png"), filename="oyun.png")

            await interaction.channel.send(files=[dosya_banner, dosya_topluluk], embeds=[embed1, embed2])

            dosya_oyun = discord.File(os.path.join("textures", "topluluk.png"), filename="topluluk.png")
            await interaction.channel.send(file=dosya_oyun, embed=embed3)

        except Exception as e:
            await interaction.followup.send(f"❌ Hata oluştu: {e}", ephemeral=True)

    @discord.ui.button(label="📖 Rol Terimleri Kur", style=discord.ButtonStyle.secondary, custom_id="kur_rolterimleri")
    async def btn_rolterimleri(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        try:
            uyari_metni = "⚠️   ```Sunucumuza girip rol yapmaya başlamadan önce mutlaka bu kanalı okumanız ve kuralları anlamanızı beklemekteyiz. Sunucuya girip rol yapmaya başladığınızda bu kuralları bildiğiniz ve okuduğunuz varsayılmaktadır.
    await bot.add_cog(KurulumCog(bot))
