import requests

from app.settings import settings


class Telegram:

    @staticmethod
    def send(text: str) -> bool:
        if not settings.TELEGRAM_BOT_TOKEN:
            print("Telegram bot token bulunamadı.")
            return False

        if not settings.TELEGRAM_CHANNEL_ID:
            print("Telegram kanal ID bulunamadı.")
            return False

        url = (
            f"https://api.telegram.org/bot"
            f"{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        )

        payload = {
            "chat_id": settings.TELEGRAM_CHANNEL_ID,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }

        try:
            response = requests.post(
                url,
                json=payload,
                timeout=20,
            )

            if response.ok:
                print("✅ Telegram mesajı gönderildi.")
                return True

            print(response.text)
            return False

        except Exception as e:
            print(e)
            return False
