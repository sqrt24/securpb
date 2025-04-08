from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from redis import Redis


@login_required(login_url="/admin/login/")
def clear_cache_view(request):
    Redis.from_url(settings.REDIS_URL).flushdb()
    return redirect("/admin/")
