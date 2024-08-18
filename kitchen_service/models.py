from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.crypto import get_random_string


class Cook(AbstractUser):
    years_of_experience = models.IntegerField(default=0)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Cook"


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class DishType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE)
    cooks = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="cooked_dishes")
    ingredients = models.ManyToManyField(
        Ingredient, related_name="used_in_dishes")

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('R', 'Rejected'),
    ]

    order_number = models.CharField(max_length=10, unique=True, editable=False)
    customer_name = models.CharField(max_length=50)
    order_date = models.DateTimeField(default=timezone.now)
    dishes = models.ManyToManyField('Dish', related_name='orders')
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default='P')

    def save(self, *args, **kwargs) -> None:
        if not self.order_number:
            self.order_number = get_random_string(10).upper()
        super().save(*args, **kwargs)
