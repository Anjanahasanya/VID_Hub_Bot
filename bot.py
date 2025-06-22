from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import feedparser
from bs4 import BeautifulSoup
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN')
BLOG_FEED_URL = os.environ.get('BLOG_FEED_URL')

def extract_video_url(summary):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(summary, 'html.parser')
    iframe = soup.find('iframe')
    if iframe and 'youtube.com' in iframe.get('src', ''):
        return iframe['src']
    video = soup.find('video')
    if video:
        source = video.find('source')
        if source and 'src' in source.attrs:
            return source['src']
    return None

async def get_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Please type a video name. Example: /getvideo paint")
        return

    keyword = ' '.join(context.args).lower()
    feed = feedparser.parse(BLOG_FEED_URL)

    for entry in feed.entries:
        if keyword in entry.title.lower():
            video_url = extract_video_url(entry.summary)
            if video_url:
                await update.message.reply_text(f"🎥 Here’s your video:\n{video_url}")
            else:
                await update.message.reply_text("✅ Found the post but no video detected.")
            return

    await update.message.reply_text("❌ No video found with that name.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("getvideo", get_video))
app.run_polling()
