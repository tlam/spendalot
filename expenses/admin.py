from django.contrib import admin

from expenses.models import Expense


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'category', 'cuisine', 'date', 'amount',)
    list_filter = ('category',)
    search_fields = ['cuisine', 'description']


admin.site.register(Expense, ExpenseAdmin)
