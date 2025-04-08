from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from core.worker import app

from .models import Form, Message


class InformerAPIView(APIView):

    def post(self, request, slug, *args, **kwargs):
        form = get_object_or_404(Form, slug=slug)
        data = request.POST.dict()
        message = Message.objects.create(form=form, data=data)
        app.send_task(
            "send_message_task",
            kwargs={
                "message_id": message.id,
            },
        )
        return Response({"message_id": message.id})
