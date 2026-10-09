from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Transaction, Category, Budget

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["title", "amount", "kind", "category", "date", "notes"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.TextInput(attrs={"placeholder": "Optional note"}),
        }
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.all()
        self.fields["category"].required = False

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ["category", "monthly_limit", "month"]
        widgets = {"month": forms.DateInput(attrs={"type": "date"})}
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(kind="expense")
