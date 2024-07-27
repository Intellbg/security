import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.urls import reverse
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from datetime import datetime

from api.models import Administrator, Checkpoint
from .forms import *
from django.shortcuts import redirect, render
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader

# Uso de loggers para capturar pistas de auditoria
import logging
logger = logging.getLogger("accounts")

def login(request):
    if request.method == "POST":
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)
        if not (email and password):
            logger.warning(f"login error")
            return render(request, "login.html", {"error": "Error de parámetros"})
        user = authenticate(username=email, password=password)
        if not user:
            # Uso de loggers para capturar pistas de auditoria
            logger.warning(f"login error")
            return render(request, "login.html", {"error": "Usuario Inválido"})
        if user.is_staff:
            logger.info(f"{user.id} staff login success")
            return HttpResponseRedirect(reverse("admin:index"))
        if not (
            Administrator.objects.filter(user=user).exists() #Uso de query de ORM para evitar inyección SQL
            or Checkpoint.objects.filter(user=user).exists() #Uso de query de ORM para evitar inyección SQL
        ):
            logger.warning(f"{user.id} login error")
            return render(request, "login.html", {"error": "Sin Permisos"})
        auth_login(request, user)
        logger.info(f"{user.id} login success")
        return HttpResponseRedirect("/")
    return render(request, "login.html")


def logout(request):
    logger.info(f"{request.user.id} logout")
    auth_logout(request)
    return HttpResponseRedirect("/login/")


def terms(request):
    return render(request, "terms_and_conditions.html")


def enviar_email_reset_password(person):
    subject, from_email, to = (
        "Recuperación contraseña cuenta PASSE",
        "Passe <" + settings.EMAIL_HOST_USER + ">",
        person.user.email,
    )
    site = settings.MY_DOMAIN
    link = site + "/restore-password/" + person.id + "/"
    context = {"link": link, "customer": person.full_name()}
    html_content = loader.render_to_string("email/reset_password.html", context)
    try:
        msg = EmailMultiAlternatives(
            subject,
            None,
            from_email,
            [to],
            headers={
                "X-Priority": "Medium",
                "User-Agent": "Zoho Mail",
                "X-Mailer": "Zoho Mail",
            },
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    except Exception as e:
        print(e)
        print("Error al enviar el email de reset_password")
        return False

    customer.reset_time = datetime.now()
    customer.save()
    return True


def enviar_email_verificacion(person):
    subject, from_email, to = (
        "Verificación de Cuenta PASSE",
        "Passe <" + settings.EMAIL_HOST_USER + ">",
        person.user.email,
    )
    site = settings.MY_DOMAIN
    link = (
        site
        + "/validate-email/"
        + customer.verification_hash
        + "/passe-app/"
        + customer.slug
        + "/"
    )
    context = {
        "link_verificacion": link,
        "customer": customer.full_name(),
        "site": site,
    }

    html_content = loader.render_to_string("email/verify.html", context)
    try:
        msg = EmailMultiAlternatives(
            subject,
            None,
            from_email,
            [to],
            headers={
                "X-Priority": "Medium",
                "User-Agent": "Zoho Mail",
                "X-Mailer": "Zoho Mail",
            },
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    except Exception as e:
        print(e)
        print("Error al enviar el email de verificacion")
        return False

    return True


def verificar_email(request, hash_validation, slug):
    if request.method == "GET":
        customer = (
            Person.objects.all()
            .filter(verification_hash=hash_validation, slug=slug)
            .first()
        )

        if not customer:
            return redirect("/NotFound/")

        if hash_validation == "0000000" or customer.active:
            usuario = customer.full_name()
            return custom_redirect("used_verification", q=usuario, code=hash_validation)

        if not customer.active:
            customer.active = True
            customer.save()
            usuario = customer.full_name()
            return custom_redirect(
                "verification_success", q=usuario, code=hash_validation
            )

    return redirect("/NotFound/")


def verification_success(request):
    if request.method == "GET":
        usuario = request.GET.get("q", None)
        code = request.GET.get("code", None)

        if Person.objects.all().filter(verification_hash=code, active=True).first():
            return render(request, "success_verification.html", {"usuario": usuario})
    return redirect("/NotFound/")


def used_verification(request):
    if request.method == "GET":
        usuario = request.GET.get("q", None)
        code = request.GET.get("code", None)
        if Person.objects.all().filter(verification_hash=code, active=True).first():
            return render(request, "used_verification.html", {"usuario": usuario})
    return redirect("/NotFound/")


def register_success(request, slug_new):
    if slug_new:
        customer = Person.objects.all().filter(slug=slug_new).first()
        if customer:
            return render(
                request, "success_registration.html", {"customer": customer.full_name()}
            )
    return HttpResponseRedirect("/NotFound/")


def restore_password(request, slug_customer):
    if slug_customer:
        person = (
            Person.objects.all()
            .filter(slug=slug_customer)
            .first()
        )
        if person:
            if request.method == "POST":
                form = ResetPasswordPersonForm(data=request.POST)
                if form.is_valid():
                    new_password = form.cleaned_data["new_password1"]
                    person.set_password(new_password)
                    person.save()
                    person.save()
                    return HttpResponseRedirect(reverse("success_reset_password"))
                else:
                    args = {}
                    args["form"] = form
                    args["slug"] = person.slug
                    return render(request, "customer_reset_password.html", args)

            args = {}
            args["form"] = ResetPasswordPersonForm(
                initial={"reset_hash": person.reset_hash}
            )
            args["slug"] = person.slug
            return render(request, "customer_reset_password.html", args)

    return redirect("/NotFound/")


def success_reset_password(request):
    if request.method == "GET":
        return render(request, "success_reset_password.html", {})
    return redirect("/NotFound/")


def auth_pusher(request):
    if request.user:
        if request.user.is_authenticated:
            channel = request.POST.get("channel_name", None)
            socket_id = request.POST.get("socket_id", None)
            if channel and socket_id:
                auth = pusher_client.authenticate(channel=channel, socket_id=socket_id)
                return HttpResponse(json.dumps(auth), content_type="application/json")
    return JsonResponse({"message": "No Authenticated"})


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login/")
    if request.user.is_staff:
        return HttpResponseRedirect("/admin/")
    if Checkpoint.objects.filter(user=request.user).exists():
        request.session.set_expiry(3154000000)
        return redirect("guard_index")
    return render(request, "header.html")


def custom_404(request):
    return render(request, "404.html", {})


def handlerError404(request, exception):
    return render(request, "404.html", status=404)


def handlerError500(request):
    return render(request, "500.html", status=500)
