from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.urls import reverse
from decimal import Decimal


class Cook(AbstractUser):
    years_of_experience = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)])
    photo = models.ImageField(upload_to="cooks/", default="cooks/default.jpg")
    facebook_link = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        default='https://www.facebook.com/'
    )
    instagram_link = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        default='https://www.instagram.com/'
    )
    twitter_link = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        default='https://www.twitter.com/'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

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
    MEAL_TIMES = [
        ("BF", "Breakfast"),
        ("LN", "Lunch"),
        ("DN", "Dinner"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2,
                                validators=[MinValueValidator(0.01)])
    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE)
    cooks = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="cooked_dishes")
    ingredients = models.ManyToManyField(
        Ingredient, related_name="used_in_dishes")
    is_popular = models.BooleanField(default=False)
    meal_time = models.CharField(max_length=2, choices=MEAL_TIMES, default="LN")
    image = models.ImageField(upload_to="dishes/", default="dishes/default.jpg")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("kitchen_service:order", args=[str(self.id)])


class Order(models.Model):
    STATUS_CHOICES = [
        ("P", "Pending"),
        ("C", "Completed"),
        ("R", "Rejected"),
    ]

    order_number = models.CharField(max_length=10, unique=True, editable=False)
    customer_name = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r"^[A-Za-zА-Яа-яЁё]+$",
                message="The name field must contain only letters.",
            )
        ]
    )
    order_date = models.DateTimeField(default=timezone.now)
    dishes = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="orders")
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=8, decimal_places=2, editable=False)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default="P")
    cook = models.ForeignKey(Cook, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if self.dishes and self.quantity:
            self.total_price = Decimal(self.quantity) * self.dishes.price
        if not self.order_number:
            self.order_number = get_random_string(10).upper()
        super().save(*args, **kwargs)
