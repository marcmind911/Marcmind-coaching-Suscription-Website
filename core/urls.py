from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"), 
    path("booking/",views.booking, name="booking"),
    path("french/",views.french, name="french"),
    path("spanish/",views.spanish, name="spanish"),
    path("english/",views.english, name="english"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("signup/", views.signup, name="signup"),
    path("username-reminder/", views.username_reminder, name="username_reminder"),
    path("checkout/<int:service_id>/<str:provider>/", views.checkout, name="checkout"),
    path("payment/paystack/callback/", views.paystack_callback, name="paystack_callback"),
    path("payment/stripe/success/", views.stripe_success, name="stripe_success"),
    path("payment/stripe/webhook/", views.stripe_webhook, name="stripe_webhook"),
    path("whatsapp/", views.whatsapp, name="whatsapp"),
    path("mentorship/", views.mentorship, name="mentorship"),
    path("library/", views.library, name="library"),
    path("username-reminder/done/",lambda request: render( request, "username_reminder_done.html"),name="username_reminder_done"),
   
]
