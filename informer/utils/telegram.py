import requests


def send_message(chat_id: str, message: str, bot_token: str, message_thread_id: str | int | None = None):
    try:
        payload = {
            "chat_id": chat_id,
            "text": message,
        }
        if message_thread_id:
            payload["message_thread_id"] = (message_thread_id,)
        response = requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data=payload,
            timeout=5,
        )
        return response.json()
    except Exception as e:
        return str(e)
