from typing import Optional
from django import forms
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit, HTML
from django.contrib.auth.forms import (
    AuthenticationForm,
    SetPasswordForm,
    PasswordResetForm,
    UserCreationForm
)
from kitchen_service.models import Order, Dish


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer_name", "quantity", "cook"]
        labels = {
            "cook": "Choose a chef"
        }

    def __init__(
            self, *args, dish: Optional[Dish] = None, customer: Optional[get_user_model] = None,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        if customer:
            self.fields["customer_name"].initial = customer.first_name
            self.fields["customer_name"].disabled = True
        if dish:
            self.fields["cook"].queryset = dish.cooks.all()
        else:
            self.fields["cook"].queryset = get_user_model().objects.filter(
                is_cook=True
            )
        self.fields["cook"].empty_label = None
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "order-form"
        self.helper.html5_required = True

        self.helper.layout = Layout(
            Field("customer_name", placeholder="Enter your name"),
            Field("quantity"),
            Field("cook"),
            ButtonHolder(
                Submit(name="submit", value="Order a dish")
            )
        )


class CookUpdateForm(forms.ModelForm):
    excluded_fields_for_non_cooks = [
        "years_of_experience", "photo", "facebook_link",
        "instagram_link", "twitter_link"
    ]

    class Meta:
        model = get_user_model()
        fields = [
            "username", "first_name", "last_name", "email",
            "years_of_experience", "photo", "facebook_link",
            "instagram_link", "twitter_link"
        ]

    def __init__(self, *args, is_cook: bool = False, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "base-form"
        self.fields["username"].help_text = ""
        self.fields["photo"].widget.attrs.update({
            "class": "form-control-file"
        })

        if not is_cook:
            for field in self.excluded_fields_for_non_cooks:
                self.fields.pop(field)

        for field_name, field in self.fields.items():
            if field_name != "photo":
                field.widget.attrs.update({"class": "form-control"})

        self.helper.add_input(Submit(
            "submit",
            "Save Changes",
            css_class="btn btn-primary w-100 mt-3"
        ))


class CookAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "base-form"
        self.helper.html5_required = True
        self.helper.form_show_labels = False
        self.helper.form_show_errors = False

        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {"class": "form-control", "placeholder": f"{field.label}"}
            )

        self.helper.layout = Layout(
            HTML(
                """
                {% if form.errors %}
                    <p class="error-message">
                        Invalid username or password. Please try again.
                    </p>
                {% endif %}
                """
            ),
            Field("username"),
            Field("password"),
            Submit(
                "submit",
                "Log in",
                css_class="button-submit btn btn-primary w-100 mt-3"
            )
        )


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "base-form"
        self.helper.html5_required = True
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            Field(
                "email",
                placeholder="Email address",
                css_class="form-control"
            ),
            Submit(
                "submit",
                "Send an email",
                css_class="button-submit btn btn-primary w-100 mt-3"
            )
        )


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "base-form"
        self.helper.html5_required = True
        self.helper.form_show_labels = False
        self.helper.form_show_errors = False
        self.fields["new_password1"].help_text = ""
        self.fields["new_password2"].help_text = ""

        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {"class": "form-control", "placeholder": f"{field.label}"}
            )
        self.helper.layout = Layout(
            HTML(
                """
                {% if form.errors %}
                    {% for field, errors in form.errors.items %}
                        {% for error in errors %}
                            <p class="error-message">{{ error }}</p>
                        {% endfor %}
                    {% endfor %}
                {% endif %}
                """
            ),
            Field("new_password1"),
            Field("new_password2"),
            Submit(
                "submit",
                "Change Password",
                css_class="button-submit btn btn-primary w-100 mt-3"
            )
        )


class CookRegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            "username", "email", "first_name",
            "last_name", "password1", "password2"
        ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "base-form"
        self.helper.html5_required = True
        self.helper.form_show_labels = False
        self.fields["username"].help_text = ""
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                "class": "form-control",
                "required": "required",
                "placeholder": f"{field.label}"
            })

        self.helper.layout = Layout(
            Field("username"),
            Field("email"),
            Field("first_name"),
            Field("last_name"),
            Field("password1"),
            Field("password2", ),
            Submit(
                "submit",
                "Register",
                css_class="button-submit btn btn-primary w-100 mt-3"
            )
        )
