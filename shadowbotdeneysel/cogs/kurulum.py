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
        await interaction.response.defer(ephemeral=True) # Resim yükleneceği için çökme önleyici
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
            
            # Gerekli 3 PNG dosyasını kontrol ediyoruz
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

    # --- YENİ BÖLÜM: ROL TERİMLERİ KOMUTU ---
    @discord.ui.button(label="📖 Rol Terimleri Kur", style=discord.ButtonStyle.secondary, custom_id="kur_rolterimleri")
    async def btn_rolterimleri(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        try:
            uyari_metni = "⚠️   ```Sunucumuza girip rol yapmaya başlamadan önce mutlaka bu kanalı okumanız ve kuralları anlamanızı beklemekteyiz. Sunucuya girip rol yapmaya başladığınızda bu kuralları bildiğiniz ve okuduğunuz varsayılmaktadır.```   "

            embed = discord.Embed(
                title="📖 Rol Terimleri",
                color=0x2b2d31
            )
            embed.add_field(name="OOC", value="Rol dışı. Gerçek hayat konuşmaları ve rolü etkilemeyen şeyler.", inline=False)
            embed.add_field(name="IC", value="Rol içi. Karakterin yaptığı her şey.", inline=False)
            embed.add_field(name="/me", value="Karakterinin yaptığı hareketi yazarsın.\n**Örnek:** /me kelepçeyi çıkarıp kişiyi kelepçeler.", inline=False)
            embed.add_field(name="/do", value="Ortamı anlatır veya soru sorar.\n**Örnek:** /do Üzerinde ne var?", inline=False)
            embed.add_field(name="//", value="OOC mesaj atmak için kullanılır.", inline=False)
            embed.add_field(name="Fail RP", value="Mantıksız ve gerçekçi olmayan rol yapmak.", inline=False)
            embed.add_field(name="Metagaming (MG)", value="Rol dışından öğrendiğin bilgiyi rolde kullanmak.", inline=False)
            embed.add_field(name="Powergaming (PG)", value="Karakterinin yapamayacağı şeyleri yapması.", inline=False)
            embed.add_field(name="Combat Log (CL)", value="Ceza, ölüm veya sorgudan kaçmak için oyundan çıkmak.", inline=False)
            embed.add_field(name="Fear RP", value="Korkulacak durumda karakterinin korkmasını oynamak.", inline=False)
            embed.add_field(name="Pain RP", value="Yaralandığında acıyı role yansıtmak.", inline=False)
            embed.add_field(name="CK (Character Kill)", value="Karakterin kalıcı olarak ölmesi.", inline=False)
            embed.add_field(name="NLR (New Life Rule)", value="Öldükten sonra eski hayatını ve yaşananları unutmak.", inline=False)
            embed.add_field(name="IC-OOC Mixing", value="Gerçek hayat ile rolü birbirine karıştırmak.", inline=False)
            embed.add_field(name="RDM (Random Deathmatch)", value="Sebepsiz yere saldırmak veya öldürmek.", inline=False)
            embed.add_field(name="Retarded RP", value="Troll, aşırı saçma ve role uymayan davranışlar yapmak.", inline=False)
            embed.add_field(name="Refuse RP", value="Mantıklı sebep olmadan rolü reddetmek.", inline=False)
            embed.add_field(name="Ghost RP", value="IC'de gerçekleştirilmemiş bir olaya hayali bir durum veya eylem entegre ederek onu yaşanılmış ve gerçekleşmiş gibi göstermek.", inline=False)
            embed.add_field(name="Shoot to Kill", value="Rol yapmadan direkt çatışıp öldürmeye çalışmak.", inline=False)
            embed.add_field(name="Shoot to Roleplay", value="/me ve /do kullanarak yapılan, rol destekli çatışma.", inline=False)
            embed.add_field(name="GOOA (Gun Out Of Ass)", value="Üzerinde olmadığı halde silah çıkarmak veya alınan silahı tekrar kullanmak.", inline=False)
            embed.add_field(name="Revenge Kill (RK)", value="Seni öldüren kişiden yeniden doğduktan sonra intikam almaya çalışmak. NLR ihlalidir.", inline=False)
            
            link_metni = "\n<:shadowroleplay:1503056096552685638> Rol terimlerinin daha detaylı hali için: <:shadowroleplay:1503056096552685638>\nhttps://docs.google.com/document/d/1jyY5_mfLW9jdPucGdslNwLY22TrHsCeGu0qkaG7vavI/edit?tab=t.0"

            dosya_yolu = os.path.join("textures", "rolterimleri.png")
            if os.path.exists(dosya_yolu):
                dosya = discord.File(dosya_yolu, filename="rolterimleri.png")
                # Uyarı, embed, link ve görsel (dosya) tek mesajda birleşiyor
                await interaction.channel.send(content=f"{uyari_metni}\n\n{link_metni}", embed=embed, file=dosya)
            else:
                await interaction.channel.send(content=f"{uyari_metni}\n\n{link_metni}", embed=embed)
                
            await interaction.followup.send("✅ Rol Terimleri paneli bu kanala başarıyla kuruldu.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Hata oluştu: {e}", ephemeral=True)


# --- COG TANIMLAMASI ---
class KurulumCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="kurulum", description="Tüm modüllerin tek bir noktadan kurulmasını sağlayan merkezi menü.")
    async def ana_kurulum(self, interaction: discord.Interaction):
        # Yetki Kontrolü
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
