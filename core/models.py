from django.conf import settings
from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    amount = models.PositiveIntegerField(help_text="Amount in smallest currency unit (e.g. 5000 = ₦50.00 if using kobo)")
    currency = models.CharField(max_length=3, default="NGN")
    stripe_price_id = models.CharField(max_length=120, blank=True)
    active = models.BooleanField(default=True)
    def __str__(self): return self.name

class Purchase(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    provider = models.CharField(max_length=20)
    reference = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.user} – {self.service} ({self.status})"
