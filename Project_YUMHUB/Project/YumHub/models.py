from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    username = models.CharField(unique=True, max_length=50)
    user_type = models.CharField(choices=USER_TYPE_CHOICES, default='user', max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.username
    
class Dish(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='dishes')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who placed the order
    status = models.CharField(max_length=50, choices=(('placed', 'Placed'), ('cancelled', 'Cancelled'), ('completed', 'Completed')), default='placed')
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # Order this item belongs to
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)  # Dish in the order
    quantity = models.PositiveIntegerField()
