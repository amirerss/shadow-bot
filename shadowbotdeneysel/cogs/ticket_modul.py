import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
import io
import datetime
import json
import os

YETKILI_ROLLER = [1496628714413228072]
TICKET_KATEGORI_ID = 1545874864747843614
TICKET_PANEL_KANAL_ID = 1545874681268146176
TICKET_LOG_KANAL_ID = 1545874651832524821
TRANSCRIPT_KANAL_ID = 1545874999934459984

def get_next_ticket_id(guild_id: int):
    dosya_adi = "ticket_data.json"
    veri = {}

    if os.path.exists(dosya_adi):
        try:
            with open(dosya_adi, "r", encoding="utf-8") as f:
                veri = json.load(f)
        except json.JSONDecodeError:
            veri = {}

    guild_str = str(guild_id)
    if guild_str not in veri:
        veri[guild_str] = {"son_ticket": 0}

    veri[guild_str]["son_ticket"] += 1

    with open(dosya_adi, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=4)

    return f"{veri[guild_str]['son_ticket']:04d}"

class TicketKapatOnay(View):
    def __init__(self, cog):
        super().__init__(timeout=120)
        self.cog = cog

    @discord.ui.button(label="✔️ Kapat", style=discord.ButtonStyle.danger)
    async def evet_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="⚠️ Ticket kapatılıp arşivleniyor, medya dosyalarının boyutuna göre bu işlem birkaç saniye sürebilir...", view=None)

        await self.cog.ticket_log("🔒 Ticket Kapatıldı", f"**Kanal:** {interaction.channel.name}\n**Kapatan:** {interaction.user.mention}", discord.Color.red())
        await self.cog.transcript_al_ve_gonder(interaction.channel)

        await interaction.channel.delete(reason=f"{interaction.user.name} tarafından kapatıldı.")

    @discord.ui.button(label="❌ İptal", style=discord.ButtonStyle.secondary)
    async def hayir_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="❌ Kapatma işlemi iptal edildi.", view=None)

class TicketKontrol(View):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="🔒 Ticket'ı Kapat", style=discord.ButtonStyle.danger, custom_id="ticket_kapat_btn")
    async def kapat_buton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("⚠️ Bu destek talebini kapatmak istediğine emin misin?", view=TicketKapatOnay(self.cog), ephemeral=True)

class TicketPanel(View):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="📩 Destek Talebi Oluştur", style=discord.ButtonStyle.secondary, custom_id="ticket_ac_btn")
    async def ac_buton(self, interaction: discord.Interaction, button: discord.ui.Button):
        kategori = self.cog.bot.get_channel(TICKET_KATEGORI_ID)
        guild = interaction.guild

        for kanal in guild.text_channels:
            if kanal.name.startswith("ticket-"):
                if kanal.overwrites_for(interaction.user).read_messages:
                    await interaction.response.send_message(f"❌ Zaten açık bir destek talebin var: {kanal.mention}", ephemeral=True)
                    return

        ticket_id = get_next_ticket_id(guild.id)
        kanal_ismi = f"ticket-{ticket_id}"

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        for rol_id in YETKILI_ROLLER:
            yetkili_rol = guild.get_role(rol_id)
            if yetkili_rol:
                overwrites[yetkili_rol] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        ticket_kanal = await guild.create_text_channel(
            name=kanal_ismi,
            category=kategori,
            overwrites=overwrites
        )

        embed = discord.Embed(
            title=f"Destek Talebi | #{ticket_id}",
            description="Hoş geldin!\n\nLütfen sorununu detaylıca açıkla, yetkili ekibimiz en kısa sürede seninle ilgilenecektir.",
            color=0x2b2d31
        )

        await ticket_kanal.send(
            content=f"{interaction.user.mention}",
            embed=embed,
            view=TicketKontrol(self.cog)
        )

        await interaction.response.send_message(f"✅ Ticket başarıyla oluşturuldu: {ticket_kanal.mention}", ephemeral=True)
        await self.cog.ticket_log("🎫 Yeni Ticket Açıldı", f"**Kanal:** {ticket_kanal.mention}\n**Açan:** {interaction.user.mention}", discord.Color.green())

class TicketCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bellenen_hareketler = {}
        self.bot.add_view(TicketPanel(self))
        self.bot.add_view(TicketKontrol(self))

    async def ticket_log(self, baslik, aciklama, renk):
        log_kanal = self.bot.get_channel(TICKET_LOG_KANAL_ID)
        if log_kanal:
            embed = discord.Embed(title=baslik, description=aciklama, color=renk, timestamp=datetime.datetime.now())
            await log_kanal.send(embed=embed)

    async def transcript_al_ve_gonder(self, kanal):
        mesajlar = [msg async for msg in kanal.history(limit=None, oldest_first=True)]
        transcript = f"--- {kanal.name} TAM TİCKET DÖKÜMÜ ---\n\n"

        kaydedilecek_dosyalar = []
        MAX_BOYUT = 24 * 1024 * 1024  # 24 MB sınır

        for m in mesajlar:
            tarih = m.created_at.strftime("%d.%m.%Y %H:%M")
            icerik = m.clean_content if m.clean_content else "*[Sadece Görsel/Dosya]*"
            satir = f"[{tarih}] {m.author.name}: {icerik}"

            if m.attachments:
                ek_isimleri = []
                for ek in m.attachments:
                    if ek.size > MAX_BOYUT:
                        ek_isimleri.append(f"{ek.filename} (⚠️ 24MB'dan büyük, indirilemedi)")
                    else:
                        ek_isimleri.append(ek.filename)
                        try:
                            veri = await ek.read()
                            yeni_isim = f"{m.author.name}_{ek.filename}"
                            kaydedilecek_dosyalar.append(discord.File(io.BytesIO(veri), filename=yeni_isim))
                        except Exception as e:
                            print(f"Dosya indirilemedi: {e}")

                satir += f"\n   ↳ [EKLENTİLER]: {', '.join(ek_isimleri)}"

            transcript += satir + "\n"

        hareketler = self.bellenen_hareketler.get(kanal.id, [])
        if hareketler:
            transcript += "\n\n--- SİLİNEN VE DÜZENLENEN MESAJ KAYITLARI ---\n\n"
            for hareket in hareketler:
                transcript += hareket + "\n\n"

        transcript_dosya = discord.File(io.BytesIO(transcript.encode('utf-8')), filename=f"transcript-{kanal.name}.txt")
        transcript_kanal = self.bot.get_channel(TRANSCRIPT_KANAL_ID)

        if transcript_kanal:
            await transcript_kanal.send(content=f"📁 **{kanal.name}** kapatıldı. Metin arşivi ektedir.", file=transcript_dosya)

            if kaydedilecek_dosyalar:
                for i in range(0, len(kaydedilecek_dosyalar), 10):
                    grup = kaydedilecek_dosyalar[i:i+10]
                    await transcript_kanal.send(content=f"🖼️ **{kanal.name}** Medya Dosyaları ({i+1}-{i+len(grup)}):", files=grup)

        if kanal.id in self.bellenen_hareketler:
            del self.bellenen_hareketler[kanal.id]

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or not isinstance(after.channel, discord.TextChannel): return
        if before.content == after.content: return

        if after.channel.name.startswith("ticket-"):
            if after.channel.id not in self.bellenen_hareketler:
                self.bellenen_hareketler[after.channel.id] = []

            zaman = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
            orijinal = before.clean_content if before.clean_content else "*[Sadece Görsel/Dosya]*"
            yeni_hali = after.clean_content if after.clean_content else "*[Sadece Görsel/Dosya]*"

            log_metni = (
                f"[{zaman}] ✏️ [DÜZENLENDİ] {before.author.name}:\n"
                f" - Orijinal: {orijinal}\n"
                f" - Yeni Hali: {yeni_hali}"
            )

            if before.attachments:
                ekler = " | ".join([ek.filename for ek in before.attachments])
                log_metni += f"\n - Orijinal Eklentiler: {ekler}"

            self.bellenen_hareketler[after.channel.id].append(log_metni)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot or not isinstance(message.channel, discord.TextChannel): return

        if message.channel.name.startswith("ticket-"):
            if message.channel.id not in self.bellenen_hareketler:
                self.bellenen_hareketler[message.channel.id] = []

            zaman = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
            silinen = message.clean_content if message.clean_content else "*[Sadece Görsel/Dosya]*"

            log_metni = (
                f"[{zaman}] 🗑️ [SİLİNDİ] {message.author.name}:\n"
                f" - Silinen Mesaj: {silinen}"
            )

            if message.attachments:
                ekler = " | ".join([ek.filename for ek in message.attachments])
                log_metni += f"\n - Silinen Eklentiler: {ekler}"

            self.bellenen_hareketler[message.channel.id].append(log_metni)

    ticket_grup = app_commands.Group(name="ticket", description="Ticket yönetim komutları")

    @ticket_grup.command(name="claim", description="Ticket'ı üzerine alırsın.")
    async def claim(self, interaction: discord.Interaction):
        if not interaction.channel.name.startswith("ticket-"):
            return await interaction.response.send_message("❌ Bu komut sadece ticket kanallarında kullanılabilir.", ephemeral=True)

        yeni_isim = f"{interaction.channel.name}-claimed"
        await interaction.channel.edit(name=yeni_isim)
        await interaction.response.send_message(f"✅ {interaction.user.mention} bu ticket ile ilgileniyor.")
        await self.ticket_log("🙋‍♂️ Ticket Üstlenildi", f"**Kanal:** {interaction.channel.mention}\n**Üstlenen:** {interaction.user.mention}", discord.Color.gold())

    @ticket_grup.command(name="add", description="Ticket'a başka birini eklersin.")
    async def add(self, interaction: discord.Interaction, uye: discord.Member):
        if not interaction.channel.name.startswith("ticket-"):
            return await interaction.response.send_message("❌ Sadece ticket kanallarında çalışır.", ephemeral=True)

        await interaction.channel.set_permissions(uye, read_messages=True, send_messages=True)
        await interaction.response.send_message(f"✅ {uye.mention} ticket'a dahil edildi.")
        await self.ticket_log("➕ Kullanıcı Eklendi", f"**Kanal:** {interaction.channel.mention}\n**Eklenen:** {uye.mention}\n**Ekleyen:** {interaction.user.mention}", discord.Color.blue())

    @ticket_grup.command(name="remove", description="Ticket'tan birini çıkarırsın.")
    async def remove(self, interaction: discord.Interaction, uye: discord.Member):
        if not interaction.channel.name.startswith("ticket-"):
            return await interaction.response.send_message("❌ Sadece ticket kanallarında çalışır.", ephemeral=True)

        await interaction.channel.set_permissions(uye, read_messages=False, send_messages=False)
        await interaction.response.send_message(f"❌ {uye.mention} ticket'tan çıkarıldı.")
        await self.ticket_log("➖ Kullanıcı Çıkarıldı", f"**Kanal:** {interaction.channel.mention}\n**Çıkarılan:** {uye.mention}\n**Çıkaran:** {interaction.user.mention}", discord.Color.orange())

    @ticket_grup.command(name="close", description="Ticket'ı slash komutu ile kapatırsın.")
    async def close(self, interaction: discord.Interaction):
        if not interaction.channel.name.startswith("ticket-"):
            return await interaction.response.send_message("❌ Sadece ticket kanallarında çalışır.", ephemeral=True)

        await interaction.response.send_message("⚠️_Bu destek talebini kapatmak istediğine emin misin?", view=TicketKapatOnay(self), ephemeral=True)

async def setup(bot):
    await bot.add_cog(TicketCog(bot))