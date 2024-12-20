import os
from decimal import Decimal
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, RegexValidator


def user_directory_path(instance: "Cook", filename: str) -> str:
    username_slug = slugify(instance.username)
    return os.path.join("cooks", username_slug, filename)


class Cook(AbstractUser):
    name_validator = RegexValidator(
        regex=r"^[A-Za-z]+$",
        message="Only alphabetic characters are allowed."
    )

    @staticmethod
    def _custom_capitalize(name: str) -> str:
        if not name:
            return name
        return name[0].upper() + name[1:].lower()

    first_name = models.CharField(max_length=30, validators=[name_validator])
    last_name = models.CharField(max_length=30, validators=[name_validator])
    email = models.EmailField(unique=True)
    years_of_experience = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        db_index=True
    )
    photo = models.ImageField(
        upload_to=user_directory_path,
        default="cooks/default.jpg"
    )
    facebook_link = models.URLField(default="https://www.facebook.com/")
    instagram_link = models.URLField(default="https://www.instagram.com/")
    twitter_link = models.URLField(default="https://www.twitter.com/")
    is_cook = models.BooleanField(default=False, db_index=True)

    def save(self, *args, **kwargs) -> None:
        self.first_name = self._custom_capitalize(str(self.first_name))
        self.last_name = self._custom_capitalize(str(self.last_name))
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Cooks and Customers"


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> CharField:
        return self.name


class DishType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> CharField:
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
    dish_type = models.ForeignKey(
        DishType, on_delete=models.CASCADE, db_index=True)
    cooks = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="cooked_dishes", db_index=True)
    ingredients = models.ManyToManyField(
        Ingredient, related_name="used_in_dishes", db_index=True)
    is_popular = models.BooleanField(default=False, db_index=True)
    meal_time = models.CharField(
        max_length=2, choices=MEAL_TIMES, default="LN",
        db_index=True)
    image = models.ImageField(
        upload_to="dishes/", default="dishes/default.jpg"
    )

    def __str__(self) -> CharField:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("kitchen_service:order-create", args=[self.pk])


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
    dishes = models.ForeignKey(
        Dish, on_delete=models.CASCADE, related_name="orders"
    )
    quantity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)])
    total_price = models.DecimalField(
        max_digits=8, decimal_places=2, editable=False
    )
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default="P")
    cook = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
    )

    class Meta:
        indexes = [
            models.Index(fields=["order_date"]),
            models.Index(fields=["status"]),
        ]

    def save(self, *args, **kwargs) -> None:
        if self.dishes and self.quantity:
            self.total_price = Decimal(str(self.quantity)) * self.dishes.price
        if not self.order_number:
            self.order_number = get_random_string(10).upper()
        super().save(*args, **kwargs)
