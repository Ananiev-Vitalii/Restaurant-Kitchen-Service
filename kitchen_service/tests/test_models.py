from django.test import TestCase
from typing import Optional
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.contrib.auth import get_user_model
from kitchen_service.models import (
    Ingredient,
    DishType,
    Dish,
    Order
)

User = get_user_model()


class BaseTestSetup(TestCase):
    @staticmethod
    def create_cook(username: str = "cook",
                    first_name: str = "Firstname",
                    last_name: str = "Lastname",
                    email: str = "cook@example.com",
                    years_of_experience: int = 3) -> User:
        return User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password="testpass123",
            is_cook=True,
            years_of_experience=years_of_experience
        )

    @staticmethod
    def create_dish(name: str = "Default Dish",
                    description: str = "Default Description",
                    price: Decimal = Decimal("10.00"),
                    dish_type: Optional[DishType] = None,
                    is_popular: bool = False,
                    meal_time: str = "LN") -> Dish:
        dish_type = dish_type or DishType.objects.create(name="Default Type")
        return Dish.objects.create(
            name=name,
            description=description,
            price=price,
            dish_type=dish_type,
            is_popular=is_popular,
            meal_time=meal_time
        )


class CookModelTest(BaseTestSetup):
    def setUp(self) -> None:
        self.cook = self.create_cook(username="cook1", years_of_experience=5)

    def test_cook_creation(self) -> None:
        self.assertEqual(self.cook.username, "cook1")
        self.assertTrue(self.cook.is_cook)
        self.assertEqual(self.cook.years_of_experience, 5)
        self.assertEqual(str(self.cook), "Firstname Lastname")

    def test_cook_name_validator_invalid(self) -> None:
        invalid_names = ["Invalid1", "Name!", "N@me", "123", "Name#"]
        for invalid_name in invalid_names:
            with self.assertRaises(ValidationError):
                cook = User(
                    username="invalid_chef",
                    first_name=invalid_name,
                    last_name=invalid_name,
                    email="invalid_chef@example.com",
                    is_cook=True
                )
                cook.set_password("strongpassword123")
                cook.full_clean()


class DishModelTest(BaseTestSetup):
    def setUp(self) -> None:
        self.dish_type = DishType.objects.create(name="Main Course")
        self.ingredient1 = Ingredient.objects.create(name="Tomato")
        self.ingredient2 = Ingredient.objects.create(name="Cheese")
        self.cook = self.create_cook(username="cook2", years_of_experience=3)
        self.dish = self.create_dish(
            name="Pizza",
            description="Delicious cheese pizza",
            price=Decimal("12.50"),
            dish_type=self.dish_type,
            is_popular=True,
            meal_time="DN"
        )
        self.dish.cooks.add(self.cook)
        self.dish.ingredients.add(self.ingredient1, self.ingredient2)

    def test_dish_creation(self) -> None:
        self.assertEqual(self.dish.name, "Pizza")
        self.assertEqual(self.dish.description, "Delicious cheese pizza")
        self.assertEqual(self.dish.price, Decimal("12.50"))
        self.assertEqual(self.dish.dish_type, self.dish_type)
        self.assertTrue(self.dish.is_popular)
        self.assertEqual(self.dish.meal_time, "DN")
        self.assertIn(self.cook, self.dish.cooks.all())
        self.assertIn(self.ingredient1, self.dish.ingredients.all())
        self.assertIn(self.ingredient2, self.dish.ingredients.all())

    def test_get_absolute_url(self) -> None:
        expected_url = f"/order/{self.dish.pk}/create/"
        self.assertEqual(self.dish.get_absolute_url(), expected_url)

    def test_price_validation(self) -> None:
        with self.assertRaises(ValidationError):
            dish = self.create_dish(
                name="Invalid Dish",
                description="Invalid price",
                price=Decimal("0.00"),
                dish_type=self.dish_type,
                is_popular=False,
                meal_time="BF"
            )
            dish.full_clean()


class OrderModelTest(BaseTestSetup):
    def setUp(self) -> None:
        self.cook = self.create_cook(username="cook2", years_of_experience=3)
        self.dish = self.create_dish(
            name="Pasta",
            description="Italian pasta",
            price=Decimal("8.99"),
            dish_type=DishType.objects.create(name="Main Course"),
            is_popular=False,
            meal_time="LN"
        )
        self.order = Order.objects.create(
            customer_name="John Doe",
            dishes=self.dish,
            quantity=2,
            cook=self.cook
        )

    def test_order_creation(self) -> None:
        self.assertEqual(self.order.customer_name, "John Doe")
        self.assertEqual(self.order.dishes, self.dish)
        self.assertEqual(self.order.quantity, 2)
        self.assertEqual(self.order.total_price, Decimal("17.98"))
        self.assertEqual(self.order.status, "P")
        self.assertEqual(self.order.cook, self.cook)
        self.assertTrue(len(self.order.order_number) == 10)
