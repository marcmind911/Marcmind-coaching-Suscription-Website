import uuid, requests, stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .forms import SignUpForm, UsernameReminderForm
from .models import Purchase, Service

def home(request): return render(request, "landing.html", {"services": Service.objects.filter(active=True)})
def signup(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(); login(request, user); return redirect("dashboard")
    return render(request, "registration/signup.html", {"form": form})
def username_reminder(request):
    form = UsernameReminderForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        for user in User.objects.filter(email__iexact=form.cleaned_data["email"]):
            send_mail("Your MarcMind username", f"Your username is: {user.username}", settings.DEFAULT_FROM_EMAIL, [user.email])
        messages.success(request, "If an account exists for that email, we have sent a username reminder.")
        return redirect("login")
    return render(request, "registration/username_reminder.html", {"form": form})
@login_required
def dashboard(request): return render(request, "dashboard.html", {"purchases": Purchase.objects.filter(user=request.user, status=Purchase.Status.PAID), "services": Service.objects.filter(active=True)})
def checkout(request, service_id, provider):
    service = get_object_or_404(Service, id=service_id, active=True); reference = uuid.uuid4().hex
    purchase = Purchase.objects.create(user=request.user, service=service, provider=provider, reference=reference)
    if provider == "stripe":
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.create(mode="payment", line_items=[{"price_data":{"currency":service.currency.lower(),"product_data":{"name":service.name},"unit_amount":service.amount*100},"quantity":1}], success_url=settings.SITE_URL + reverse("stripe_success") + "?session_id={CHECKOUT_SESSION_ID}", cancel_url=settings.SITE_URL + reverse("booking"), metadata={"purchase_id": purchase.id})
        purchase.reference = session.id; purchase.save(update_fields=["reference"]); return redirect(session.url)
    if provider == "paystack":
        response = requests.post("https://api.paystack.co/transaction/initialize", headers={"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}, json={"email":request.user.email,"amount":service.amount,"currency":service.currency,"reference":reference,"callback_url":settings.SITE_URL + reverse("paystack_callback")}, timeout=15).json()
        if response.get("status"): return redirect(response["data"]["authorization_url"])
    purchase.delete(); messages.error(request, "Payment provider is unavailable."); return redirect("booking")
def stripe_success(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(request.GET.get("session_id", ""))
    if session.payment_status == "paid": Purchase.objects.filter(reference=session.id, user=request.user).update(status=Purchase.Status.PAID)
    return redirect("whatsapp")
def paystack_callback(request):
    ref = request.GET.get("reference", ""); response = requests.get(f"https://api.paystack.co/transaction/verify/{ref}", headers={"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}, timeout=15).json()
    if response.get("data", {}).get("status") == "success": Purchase.objects.filter(reference=ref, user=request.user).update(status=Purchase.Status.PAID); return redirect("whatsapp")
    messages.error(request, "Payment could not be verified."); return redirect("booking")
@csrf_exempt
def stripe_webhook(request):
    try: event = stripe.Webhook.construct_event(request.body, request.headers.get("Stripe-Signature"), settings.STRIPE_WEBHOOK_SECRET)
    except Exception: return HttpResponseBadRequest()
    if event["type"] == "checkout.session.completed": Purchase.objects.filter(reference=event["data"]["object"]["id"]).update(status=Purchase.Status.PAID)
    return HttpResponse(status=200)
@login_required
def whatsapp(request):
    if not Purchase.objects.filter(user=request.user, status=Purchase.Status.PAID).exists(): return redirect("dashboard")
    return redirect(f"https://wa.me/{settings.WHATSAPP_NUMBER}?text=Bonjour%20MarcMind%2C%20je%20viens%20de%20m%27inscrire.")
@login_required
def booking(request):
    services = Service.objects.filter(active=True)
    return render(request,"Booking.html",{ "purchases": Purchase.objects.filter(user=request.user,status=Purchase.Status.PAID),"services": services })
@login_required
def french(request):
    return render (request, "marcmind-fr.html")
@login_required
def spanish(request):
    return render (request, "marcmind-es.html")
@login_required
def english(request):
    return render(request,"landing.html")
@login_required
def mentorship(request):
    return render(request, "mentorship.html")
@login_required
def library(request):
    return render(request, "library.html")

def username_reminder(request):

    if request.method == "POST":

        form = UsernameReminderForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"]

            users = User.objects.filter(
                email__iexact=email
            )

            if users.exists():

                for user in users:

                    send_mail(
                        subject="Your Username",
                        message=(
                            f"Hello {user.get_full_name() or user.username},\n\n"
                            f"Your username is: {user.username}\n\n"
                            "You can now use this username to log in."
                        ),
                        from_email=None,
                        recipient_list=[user.email],
                        fail_silently=False,
                    )

            return redirect("username_reminder_done")

    else:

        form = UsernameReminderForm()

    return render(
        request,
        "username_reminder.html",
        {"form": form}
    )