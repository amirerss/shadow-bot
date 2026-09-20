import discord
from discord.ext import commands
from discord import app_commands
import os

YETKILI_ROLLER = [1483443654772396093, 1494377287666368602, 1494377031432147055]

# --- METİNLER (Sen metinleri attığında buraları güncelleyeceğiz) ---
ORTA_METIN = 
## Booster (Havalı Kişi) Avantajları;
* Sunucumuza *1 Adet* takviye gönderen kişiler, sunucumuzda özel @Havalı Kişi rolünü kazanır. Bu rol, size #┃destekçi-özel-kanalı'na erişim sağlatacaktır. (Bu kanal, sunucumuza getireceğimiz güncellemeler hakkında sadece **havalı kişilere** özel fotoğraflar veya bilgiler verecektir.)

* Sunucumuza *2 Adet* takviye gönderen kişilerin isimleri, her güncellemede haritamızda bulunan **Müze** bölümüne eklenecektir.

* Sunucumuza *3 Ay* boyunca takviye göndermiş kişilerin isinleri, her güncellemede haritamızda bulunan **Müze** bölümüne eklenecektir.

* Sunucumuza *6 Ay* boyunca takviye göndermiş kişilerin roblox karakterleri, her güncellemede haritamızda bulunan **Müze** bölümüne *heykel* olarak eklenecektir. 

* Sunucumuza *12 Ay* boyunca takviye gönderen kişilerin roblox karakterleri, her güncellemede haritamızda bulunan **Müze** bölümüne **daha büyük heykel** şeklinde eklenecektir.

* Sunucumuza *10 Adet* takviye gönderen kişilere **sadece** onlarda olacak ve kendilerinin (belirli kurallar çerçevesinde) belirlediği isme sahip *discord* rolü verilecektir. (Bu rol, 2 ay boyunca 10 takviye atan kişilerde KALICI olacaktır.)
-# 10 Takviyeye SADECE tek bir hesapla atmalısınız. Farklı hesaplar kullanmanız, veya 3. parti sitelerden satın almanız KABUL EDİLMEYECEKTİR.
ALT_METIN = 


class AvantajlarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    avantajlar_grup = app_commands.Group(name="avantajlar", description="Avantajlar paneli yönetim sistemi")

    @avantajlar_grup.command(name="kurulum", description="Avantajlar panelini bu kanala kurar.")
    async def avantajlar_kurulum(self, interaction: discord.Interaction):
        # Yetki Kontrolü
        kullanici_rolleri = [rol.id for rol in interaction.user.roles]
        if not any(rol in YETKILI_ROLLER for rol in kullanici_rolleri):
            return await interaction.response.send_message("❌ Bu komutu kullanmak için yetkiniz yok!", ephemeral=True)

        await interaction.response.defer(ephemeral=True)

        # 1. EMBED: Sadece en üst kapak fotoğrafı
        embed1 = discord.Embed(color=0x2b2d31)
        embed1.set_image(url="attachment://avantaj_ust.png")

        # 2. EMBED: Ortadaki metin ve içindeki fotoğraf
        embed2 = discord.Embed(description=ORTA_METIN, color=0x2b2d31)
        embed2.set_image(url="attachment://avantaj_orta.png")

        # 3. EMBED: En alttaki metin ve içindeki fotoğraf
        embed3 = discord.Embed(description=ALT_METIN, color=0x2b2d31)
        embed3.set_image(url="attachment://avantaj_alt.png")
        embed3.set_footer(text="Shadow Roleplay • Avantajlar")

        dosyalar = []
        gonderilecek_embedler = []
        
        # Dosyaların varlığını kontrol edip listeye ekliyoruz
        if os.path.exists("textures/avantaj_ust.png"):
            dosyalar.append(discord.File("textures/avantaj_ust.png", filename="avantaj_ust.png"))
            gonderilecek_embedler.append(embed1)
            
        if os.path.exists("textures/avantaj_orta.png"):
            dosyalar.append(discord.File("textures/avantaj_orta.png", filename="avantaj_orta.png"))
            gonderilecek_embedler.append(embed2)
        else:
            embed2.set_image(url=None)
            gonderilecek_embedler.append(embed2)
            
        if os.path.exists("textures/avantaj_alt.png"):
            dosyalar.append(discord.File("textures/avantaj_alt.png", filename="avantaj_alt.png"))
            gonderilecek_embedler.append(embed3)
        else:
            embed3.set_image(url=None)
            gonderilecek_embedler.append(embed3)

        try:
            # 3 embed kutusunu ve 3 farklı görseli aynı anda tek mesaja sabitliyoruz
            if dosyalar:
                await interaction.channel.send(files=dosyalar, embeds=gonderilecek_embedler)
            else:
                await interaction.channel.send(embeds=gonderilecek_embedler)
            
            await interaction.followup.send("✅ Avantajlar paneli başarıyla kuruldu.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Panel kurulurken hata oluştu: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(AvantajlarCog(bot))
