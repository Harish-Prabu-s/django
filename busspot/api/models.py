from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Custom User
class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name="api_user_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="api_user_set_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

# Bus model
class Bus(models.Model):
    bus_name = models.CharField(max_length=100, null=True)
    bus_number = models.CharField(max_length=50, unique=True, null=True)
    source = models.CharField(max_length=100, null=True)
    destination = models.CharField(max_length=100, null=True)
    total_seats = models.IntegerField(null=True)
    available_seats = models.IntegerField(null=True)
    departure_time = models.DateTimeField(null=True)
    arrival_time = models.DateTimeField(null=True)
    fare = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    date = models.DateField(null=True)

# Route model
class Route(models.Model):
    bus_name = models.CharField(max_length=100, null=True)
    bus_number = models.CharField(max_length=50, unique=True, null=True)
    source = models.CharField(max_length=100, null=True)
    destination = models.CharField(max_length=100, null=True)
    available_seats = models.IntegerField(null=True)
    departure_time = models.DateTimeField(null=True)
    arrival_time = models.DateTimeField(null=True)
    fare = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    date = models.DateField(null=True)

# Booking model
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    payment_status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
