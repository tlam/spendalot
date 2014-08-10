from datetime import datetime

from django.db import models

PAYMENT_CHOICES = (
    ('CA', 'Cash'),
    ('CC', 'Credit Card'),
)


class Expense(models.Model):
    description = models.CharField(max_length=200)
    payment = models.CharField(max_length=5, choices=PAYMENT_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey('categories.Category')
    created_at = models.DateTimeField(auto_now_add=True, default=datetime.now())
    updated_at = models.DateTimeField(auto_now=True, default=datetime.now())

    def __unicode__(self):
        return u'{}'.format(self.description)
