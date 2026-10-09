from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=60, unique=True)
    kind = models.CharField(max_length=10, choices=[("expense", "Expense"), ("income", "Income")], default="expense")

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return f"{self.name} ({self.kind})"

class Transaction(models.Model):
    INCOME = "income"
    EXPENSE = "expense"
    TYPES = [(INCOME, "Income"), (EXPENSE, "Expense")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    title = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    kind = models.CharField(max_length=10, choices=TYPES, default=EXPENSE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions")
    date = models.DateField(default=timezone.localdate)
    notes = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.title} — ₹{self.amount}"

class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="budgets")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="budgets")
    monthly_limit = models.DecimalField(max_digits=12, decimal_places=2)
    month = models.DateField(default=timezone.localdate, help_text="Choose a date in the month this budget applies to.")

    class Meta:
        ordering = ["-month", "category__name"]
        constraints = [models.UniqueConstraint(fields=["user", "category", "month"], name="unique_user_category_budget_month")]

    def __str__(self):
        return f"{self.category.name}: ₹{self.monthly_limit} ({self.month:%Y-%m})"

    @property
    def spent(self):
        return self.user.transactions.filter(
            kind="expense", category=self.category,
            date__year=self.month.year, date__month=self.month.month
        ).aggregate(total=models.Sum("amount"))["total"] or Decimal("0.00")

    @property
    def percent_used(self):
        if not self.monthly_limit:
            return 0
        return min(100, int((self.spent / self.monthly_limit) * 100))
