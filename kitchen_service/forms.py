from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer_name", "quantity", "cook"]
        labels = {
            "cook": "Choose a chef"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cook"].empty_label = None

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = ""
        self.helper.form_class = "order-form"
        self.helper.html5_required = True

        self.helper.layout = Layout(
            Field(
                "customer_name",
                placeholder="Enter your name",
            ),
            Field("quantity"),
            Field("cook"),
            ButtonHolder(
                Submit(
                    name="submit",
                    value="Order a dish",
                )
            )
        )
