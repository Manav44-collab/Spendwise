from django.contrib import admin
from .models import Category, Transaction, Budget

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "kind")
    list_filter = ("kind",)
    search_fields = ("name",)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "kind", "amount", "category", "date")
    list_filter = ("kind", "date", "category")
    search_fields = ("title", "user__username")

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "monthly_limit", "month")
    list_filter = ("month", "category")
