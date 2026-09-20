import discord
from discord.ext import commands
from discord import app_commands
import os

YETKILI_ROLLER = [1545845833826697296]

BLACKLIST_METNI = """# LİSTE | 1. GRUP
     
> @wzzyq **| WİZZY** {*Fail RP*}
> @heyselambenmusa **| SELAMBENMUSA** { *ERP* }
> **AMAZİNGO13579**  { *Ayrımcılık, ERP* }
> <@1086968756556812299> **| JASTEROY**  { *Topluluk Kuralları: 1-4* }
> <@1086968756556812299> **| CHAOS_INC1** { *Topluluk Kuralları: 1-4* }
> <@60768613394992332> **| SOYKAN613** { *Fail RP - Fear RP - Power Gaming* }
> <@670292858863091722> **| ALENOS** { *Topluluk Kuralları: 1-2* }
> <@870667853769101322> **| LENMA_AOVİ** { *Topluluk Kuralları: 1-3-5 / Fail RP* }
> <@1472558322619121686> **| HESAPGİTTİYENİACCAM_1234** { *Topluluk Kuralları: 4* }
> <@1350482949715267584> **| AZRLANUC** { *Topluluk Kuralları: 1-8* }
> <@1069329011253194772> **| JİTEM9** { *Topluluk Kuralları: 1-5-9-11* }
> <@979090552656113694> **| AUTRON** { *Topluluk Kuralları: 1-5 / Fail RP - Power Gaming* }
> <@1475095113977041031> **| PROKAYADEVREDE** { *Topluluk Kuralları: 4* }
> <@768075618326937621> **| YAGO** { *Topluluk Kuralları: 1-5-6-9* }
> <@788094302630838282> **| LYNX** { *Topluluk Kuralları: 1-5-9* }
> <@1001489280587288696> **| NAPHERİNE** { *Topluluk Kuralları: 1-5-9* }
> <@1426190777377230908> **| COOLKİDSFANS** { *Topluluk Kuralları: 1-2-9 / TACİZ* }
> <@1480279863238594602> **| EMİRKAN_MUSTAİNE** { *Topluluk Kuralları: 1-5-6-9-17-18-21* }
> <@1344687250721738894> **| GİRAYCANKANAL** { *Topluluk Kuralları: 1-3-5-6-8-9-11-15-17-20* }
> <@1239916919872557158> **| KAANPROXDDDD** { *Fail RP - Non-RP Davranışlar - RDM* }
> <@1354162100309590121> **| GLOBALOCCULTCOALİTİON** { *Topluluk Kuralları: 1-2-5-9* }
> <@2928661955> **| 12BARUT33** { *Topluluk Kuralları: 1-5-18* }
> <@11457710967> **| EXPLOITERS045** { *Fail RP - Hile Kullanımı* }
> <@3455418438> **| SCPSOLDİRES** { *Topluluk Kuralları: 3-5-9 / Fail RP* }
> <@960126607471829074> **| ADEN_0001** { *Topluluk Kuralları: 15 / Shadow:RP Adı altıyla başka sunuculara zarar vermek. Trollemek* }
> <@1263841215917326401> **| RZGRMRT99** { *Topluluk Kuralları: 4* }
> <@455351827660144640> **| AFRASHH** { *Topluluk Kuralları: 1* }
> <@1138033473114882078> **| BEN_MEGOLOJİ** { *Topluluk Kuralları: 1-2-9-15* }
> <@3158218406> **| ERDALMİKAİL** { *Fail RP - Baf - RP'ye Saygı Kuralı* }"""

class IlkBlacklistCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ilkblacklist", description="İlk blacklist listesini görseliyle birlikte kanala sabitler.")
    async def ilkblacklist_kur(self, interaction: discord.Interaction):
        # Yetki Kontrolü
        kullanici_rolleri = [rol.id for rol in interaction.user.roles]
        if not any(rol in YETKILI_ROLLER for rol in kullanici_rolleri):
            return await interaction.response.send_message("❌ Bu komutu kullanmak için yetkiniz yok!", ephemeral=True)

        # Sade koyu gri embed kutusu ve içine eklenecek metin
        embed = discord.Embed(
            description=BLACKLIST_METNI,
            color=0x2b2d31
        )
        embed.set_footer(text="Shadow Roleplay • Kara Liste")

        dosya_yolu = os.path.join("textures", "blacklist.png")
        
        # Eğer textures klasöründe blacklist.png varsa embed kutusunun tepe kısmına ekle
        if os.path.exists(dosya_yolu):
            dosya = discord.File(dosya_yolu, filename="blacklist.png")
            embed.set_image(url="attachment://blacklist.png")
            
            await interaction.channel.send(file=dosya, embed=embed)
            await interaction.response.send_message("✅ İlk blacklist mesajı kanala başarıyla sabitlendi.", ephemeral=True)
        else:
            await interaction.channel.send(embed=embed)
            await interaction.response.send_message("✅ Liste kuruldu ancak `textures/blacklist.png` bulunamadığı için fotoğrafsız gönderildi.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(IlkBlacklistCog(bot))
