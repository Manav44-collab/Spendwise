from datetime import date
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Sum, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import RegisterForm, TransactionForm, BudgetForm
from .models import Transaction, Category, Budget

def seed_categories():
    defaults = [
        ("Food", "expense"), ("Travel", "expense"), ("Bills", "expense"),
        ("Entertainment", "expense"), ("Shopping", "expense"), ("Health", "expense"),
        ("Education", "expense"), ("Other", "expense"), ("Salary", "income"),
        ("Freelance", "income"), ("Gift", "income"),
    ]
    for name, kind in defaults:
        Category.objects.get_or_create(name=name, defaults={"kind": kind})

def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    seed_categories()
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Welcome! Your account is ready.")
        return redirect("dashboard")
    return render(request, "expenses/register.html", {"form": form})

@login_required
def dashboard(request):
    seed_categories()
    today = timezone.localdate()
    qs = Transaction.objects.filter(user=request.user)
    month_qs = qs.filter(date__year=today.year, date__month=today.month)
    income = month_qs.filter(kind="income").aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    expense = month_qs.filter(kind="expense").aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    budgets = Budget.objects.filter(user=request.user, month__year=today.year, month__month=today.month).select_related("category")
    alerts = [b for b in budgets if b.monthly_limit and b.spent >= b.monthly_limit * Decimal("0.8")]
    recent = qs.select_related("category")[:6]
    categories = Category.objects.filter(kind="expense")
    return render(request, "expenses/dashboard.html", {
        "income": income, "expense": expense, "balance": income-expense,
        "recent": recent, "budgets": budgets, "alerts": alerts,
        "categories": categories, "month_name": today.strftime("%B %Y"),
        "expense_by_category": [
            {"name": c.name, "total": qs.filter(kind="expense", category=c, date__year=today.year, date__month=today.month).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")}
            for c in categories
        ],
    })

@login_required
def transaction_list(request):
    qs = Transaction.objects.filter(user=request.user).select_related("category")
    query = request.GET.get("q", "").strip()
    kind = request.GET.get("kind", "")
    if query:
        qs = qs.filter(Q(title__icontains=query) | Q(notes__icontains=query) | Q(category__name__icontains=query))
    if kind in ("income", "expense"):
        qs = qs.filter(kind=kind)
    return render(request, "expenses/transactions.html", {"transactions": qs, "query": query, "kind": kind})

@login_required
def transaction_create(request):
    seed_categories()
    form = TransactionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False)
        item.user = request.user
        item.save()
        messages.success(request, "Transaction saved.")
        return redirect("transactions")
    return render(request, "expenses/transaction_form.html", {"form": form, "heading": "Add transaction"})

@login_required
def transaction_update(request, pk):
    item = get_object_or_404(Transaction, pk=pk, user=request.user)
    form = TransactionForm(request.POST or None, instance=item)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Transaction updated.")
        return redirect("transactions")
    return render(request, "expenses/transaction_form.html", {"form": form, "heading": "Edit transaction"})

@login_required
def transaction_delete(request, pk):
    item = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Transaction deleted.")
        return redirect("transactions")
    return render(request, "expenses/transaction_confirm_delete.html", {"item": item})

@login_required
def budget_list(request):
    seed_categories()
    form = BudgetForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        budget = form.save(commit=False)
        budget.user = request.user
        try:
            budget.save()
            messages.success(request, "Budget saved.")
            return redirect("budgets")
        except Exception:
            form.add_error(None, "A budget for this category and month already exists.")
    budgets = Budget.objects.filter(user=request.user).select_related("category")
    return render(request, "expenses/budgets.html", {"form": form, "budgets": budgets})

@login_required
def report(request):
    today = timezone.localdate()
    qs = Transaction.objects.filter(user=request.user, date__year=today.year, date__month=today.month)
    rows = []
    for cat in Category.objects.filter(kind="expense"):
        total = qs.filter(kind="expense", category=cat).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
        if total:
            rows.append({"name": cat.name, "total": total})
    total_expense = qs.filter(kind="expense").aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    total_income = qs.filter(kind="income").aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    return render(request, "expenses/reports.html", {"rows": rows, "month_name": today.strftime("%B %Y"), "total_expense": total_expense, "total_income": total_income})
