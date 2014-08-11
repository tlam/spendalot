from django.contrib import admin

from expenses.models import Expense


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'category', 'date', 'amount',)

admin.site.register(Expense, ExpenseAdmin)
