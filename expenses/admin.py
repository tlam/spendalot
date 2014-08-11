from django.contrib import admin

from expenses.models import Expense


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'category', 'date', 'amount',)
    search_fields = ['description']

admin.site.register(Expense, ExpenseAdmin)
