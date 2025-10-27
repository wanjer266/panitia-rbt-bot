from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import requests
from bs4 import BeautifulSoup

# === TOKEN BOT TELEGRAM KAU DI SINI ===
TOKEN = "8334807197:AAFxJKaUZGU1puyz206TfGx3iLvm4-ohfzs"

# === LINK GOOGLE DRIVE UTAMA ===
MAIN_FOLDER = "https://drive.google.com/drive/folders/12clIWH8i-PT7IhyJIO7s7qIk6UZivU_H"

# === Senarai Subfolder ===
SUBFOLDERS = {
    "BANK ERPJH": "https://drive.google.com/drive/folders/xxxx",
    "BANK SOALAN UASA": "https://drive.google.com/drive/folders/yyyy",
    "BORANG TRANSIT PBD": "https://drive.google.com/drive/folders/zzzz",
    "CARTA ORGANISASI": "https://drive.google.com/drive/folders/aaaa",
    "DSKP": "https://drive.google.com/drive/folders/bbbb",
    "KERTA KERJA": "https://drive.google.com/drive/folders/cccc",
    "LAPORAN PROGRAM KECEMERLANGAN": "https://drive.google.com/drive/folders/dddd",
    "LAPORAN SEMAKAN HASIL KERJA MURID": "https://drive.google.com/drive/folders/eeee",
    "MAKLUMAT AHLI PANITIA": "https://drive.google.com/drive/folders/ffff",
    "MINIT MESYUARAT": "https://drive.google.com/drive/folders/gggg",
    "PBD (JASA & PEPERIKSAAN)": "https://drive.google.com/drive/folders/hhhh",
    "PENGURUSAN PCG": "https://drive.google.com/drive/folders/iiii",
    "PERANCANGAN STRATEGIK PANITIA": "https://drive.google.com/drive/folders/jjjj",
    "PLC PANITIA": "https://drive.google.com/drive/folders/kkkk",
    "POST MORTEM": "https://drive.google.com/drive/folders/llll",
    "TAKWIM PDPC RBT T1–T3": "https://drive.google.com/drive/folders/mmmm"
}

# === Fungsi ambil fail dari folder Drive ===
def get_drive_files(folder_url):
    html = requests.get(folder_url).text
    soup = BeautifulSoup(html, "html.parser")
    files = []
    for a in soup.find_all("a", href=True):
        if "https://drive.google.com/file" in a["href"]:
            name = a.text.strip()
            link = a["href"]
            files.append(f"📄 [{name}]({link})")
    return files[:20]

# === /start command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    row = []
    for i, (name, link) in enumerate(SUBFOLDERS.items(), start=1):
        row.append(InlineKeyboardButton(f"📁 {name}", callback_data=name))
        if i % 2 == 0:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "📚 *BOT PANITIA RBT 2025/26*\n\nPilih kategori fail di bawah untuk lihat kandungan Google Drive:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# === Callback bila tekan butang ===
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    folder_name = query.data
    folder_url = SUBFOLDERS.get(folder_name)
    files = get_drive_files(folder_url)

    if not files:
        text = f"⚠️ Tiada fail dalam folder *{folder_name}*."
    else:
        text = f"📂 *{folder_name}* — senarai fail:\n\n" + "\n".join(files)

    await query.edit_message_text(
        text=text,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

# === Setup bot ===
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_callback))

print("🤖 Bot Panitia RBT sedang berjalan...")
app.run_polling()
