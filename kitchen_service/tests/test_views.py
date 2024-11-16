from django.test import TestCase, Client
from decimal import Decimal
from django import forms
from django.contrib.auth import get_user_model
from django.urls import reverse
from kitchen_service.forms import OrderForm, CookRegistrationForm
from kitchen_service.models import Dish, DishType, Cook, Order

User = get_user_model()


class BaseTestCase(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.client = Client()
        cls.dish_type = DishType.objects.create(name="Garnish")
        cls.cook = Cook.objects.create_user(
            username="cook1",
            email="cook1@example.com",
            password="testpass123",
            is_cook=True,
            years_of_experience=5
        )
        cls.dish1 = Dish.objects.create(
            name="Salad",
            description="Fresh salad",
            price=Decimal("4.50"),
            dish_type=cls.dish_type,
            is_popular=True,
            meal_time="LN"
        )
        cls.dish1.cooks.add(cls.cook)
        cls.dish2 = Dish.objects.create(
            name="Soup",
            description="Hot soup",
            price=Decimal("3.75"),
            dish_type=cls.dish_type,
            is_popular=False,
            meal_time="DN"
        )
        cls.dish2.cooks.add(cls.cook)


class DishListViewTest(BaseTestCase):

    def test_dish_list_view_status_code(self) -> None:
        response = self.client.get(reverse("kitchen_service:index"))
        self.assertEqual(response.status_code, 200)

    def test_dish_list_view_template(self) -> None:
        response = self.client.get(reverse("kitchen_service:index"))
        self.assertTemplateUsed(response, "kitchen_service/index.html")

    def test_dish_list_view_context(self) -> None:
        response = self.client.get(reverse("kitchen_service:index"))
        self.assertIn("dish_list", response.context)
        self.assertEqual(len(response.context["dish_list"]), 2)
        self.assertIn(self.dish1, response.context["dish_list"])
        self.assertIn(self.dish2, response.context["dish_list"])


class OrderCreateViewTest(BaseTestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.dish_type_main = DishType.objects.create(name="Main Course")
        cls.cook2 = Cook.objects.create_user(
            username="cook2",
            email="cook2@example.com",
            password="testpass123",
            is_cook=True,
            years_of_experience=3
        )
        cls.dish_main = Dish.objects.create(
            name="Steak",
            description="Grilled steak",
            price=Decimal("15.00"),
            dish_type=cls.dish_type_main,
            is_popular=True,
            meal_time="DN"
        )
        cls.dish_main.cooks.add(cls.cook2)
        cls.order_create_url = reverse(
            "kitchen_service:order-create", args=[cls.dish_main.pk])

    def test_order_create_view_get(self) -> None:
        response = self.client.get(self.order_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen_service/order_form.html")
        self.assertIn("form", response.context)
        self.assertIn("dish", response.context)
        self.assertEqual(response.context["dish"], self.dish_main)

    def test_order_create_view_post_valid_data(self) -> None:
        data = {
            "customer_name": "Bob",
            "quantity": 2,
            "cook": self.cook2.pk
        }
        response = self.client.post(self.order_create_url, data)
        self.assertRedirects(response, reverse("kitchen_service:menu-list"))
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.customer_name, "Bob")
        self.assertEqual(order.quantity, 2)
        self.assertEqual(order.dishes, self.dish_main)
        self.assertEqual(order.total_price, Decimal("30.00"))
        self.assertEqual(order.status, "P")
        self.assertEqual(order.cook, self.cook2)

    def test_order_create_view_post_invalid_data(self) -> None:
        data = {
            "customer_name": "",
            "quantity": 0,
            "cook": self.cook2.pk
        }
        response = self.client.post(self.order_create_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        form: OrderForm = response.context["form"]
        self.assertIsInstance(form, OrderForm)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertIn("customer_name", form.errors)
        self.assertIn("This field is required.", form.errors["customer_name"])
        self.assertIn("quantity", form.errors)
        self.assertIn(
            "Ensure this value is greater than or equal to 1.",
            form.errors["quantity"]
        )
        self.assertEqual(Order.objects.count(), 0)


class CookRegistrationViewTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.client = Client()
        cls.register_url = reverse("kitchen_service:register")

    def test_registration_view_get(self) -> None:
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertIn("form", response.context)

    def test_registration_view_post_valid_data(self) -> None:
        data = {
            "username": "newcook2",
            "email": "newcook2@example.com",
            "first_name": "New",
            "last_name": "Cook",
            "password1": "StrongPassword123",
            "password2": "StrongPassword123"
        }
        response = self.client.post(self.register_url, data)
        self.assertRedirects(response, reverse("kitchen_service:login"))
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, "newcook2")
        self.assertEqual(user.email, "newcook2@example.com")
        self.assertTrue(user.check_password("StrongPassword123"))

    def test_registration_view_post_invalid_data(self) -> None:
        data = {
            "username": "newchef3",
            "email": "invalid-email",
            "first_name": "New",
            "last_name": "Chef",
            "password1": "password",
            "password2": "differentpassword"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        form: forms.Form = response.context["form"]
        self.assertIsInstance(form, CookRegistrationForm)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertIn("Enter a valid email address.", form.errors["email"])
        self.assertIn("password2", form.errors)

        password_error = form.errors["password2"][0]
        self.assertIn("password fields", password_error)
        self.assertIn("match", password_error)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(User.objects.count(), 0)


class CookRequiredMixinTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.client = Client()
        cls.cook = Cook.objects.create_user(
            username="cook10",
            email="cook10@example.com",
            password="testpass123",
            is_cook=True,
            years_of_experience=7
        )
        cls.non_cook = Cook.objects.create_user(
            username="user1",
            email="user1@example.com",
            password="testpass123",
            is_cook=False
        )
        cls.dish = Dish.objects.create(
            name="Burger",
            description="Beef burger",
            price=Decimal("7.50"),
            dish_type=DishType.objects.create(name="Main Course"),
            is_popular=False,
            meal_time="DN"
        )
        cls.dish.cooks.add(cls.cook)
        cls.order = Order.objects.create(
            customer_name="Charlie",
            dishes=cls.dish,
            quantity=1,
            cook=cls.cook
        )
        cls.cook_orders_url = reverse("kitchen_service:cook-orders-list")

    def test_non_cook_access(self) -> None:
        self.client.login(username="user1", password="testpass123")
        response = self.client.get(self.cook_orders_url)
        self.assertEqual(response.status_code, 404)

    def test_cook_access(self) -> None:
        self.client.login(username="cook10", password="testpass123")
        response = self.client.get(self.cook_orders_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "kitchen_service/cook_order_list.html")
        self.assertIn("order_list", response.context)
        self.assertIn(self.order, response.context["order_list"])
