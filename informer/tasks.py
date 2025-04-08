from celery import shared_task
from django.conf import settings

from project_settings.models import ProjectSettings

from .models import Message
from .utils.bitrix import BitrixSender
from .utils.telegram import send_message


@shared_task(name="send_message_task")
def send_message_task(
    message_id: int,
    ignore_sent: bool = False,
) -> dict:
    message: Message = Message.objects.filter(id=message_id).select_related("form").first()
    if message is None:
        return {
            "message_id": message_id,
            "error": "Message not found.",
        }
    if not ignore_sent and message.is_sent:
        return {
            "message_id": message_id,
            "error": "Message is already sent.",
        }
    tg_data = send_message(
        bot_token=settings.BOT_TOKEN,
        chat_id=settings.CHAT_ID,
        message_thread_id=message.form.message_thread_id,
        message=message.text,
    )
    message.mark_sent()
    project_settings = ProjectSettings.objects.first()
    bx_data = BitrixSender(
        webhook_url=project_settings.bitrix_webhook_url,
        user_id=project_settings.bitrix_user_id,
        source_id=project_settings.bitrix_source_id,
        name=message.data.get("name"),
        email=message.email,
        phone=message.phone,
        order_id=message.id,
        message_body=message.text,
    ).send_order()
    return {
        "bx_data": bx_data,
        "message_id": message_id,
        "tg_data": tg_data,
    }


@shared_task(name="resend_email_task")
def resend_email_task() -> dict[str, int]:
    resent_count = 0
    for msg in Message.objects.filter(is_sent=False, retries__lt=3).order_by("-created_at"):
        msg.send_message()
        msg.retries += 1
        msg.save()
    return {"resent_count": resent_count}
