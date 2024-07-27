from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings


@login_required()
def index_checkpoint(request):
    return render(request, "checkpoint/index.html", {"key": settings.PUSHER_KEY})


@login_required()
def operations(request):
    return render(request, "checkpoint/operations/table.html")
