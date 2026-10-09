from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="expenses/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("transactions/", views.transaction_list, name="transactions"),
    path("transactions/add/", views.transaction_create, name="transaction_add"),
    path("transactions/<int:pk>/edit/", views.transaction_update, name="transaction_edit"),
    path("transactions/<int:pk>/delete/", views.transaction_delete, name="transaction_delete"),
    path("budgets/", views.budget_list, name="budgets"),
    path("reports/", views.report, name="reports"),
]
