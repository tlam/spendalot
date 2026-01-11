# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Expense",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("description", models.CharField(max_length=200)),
                (
                    "payment",
                    models.CharField(
                        max_length=5,
                        choices=[(b"CA", b"Cash"), (b"CC", b"Credit Card")],
                    ),
                ),
                ("amount", models.DecimalField(max_digits=10, decimal_places=2)),
                ("date", models.DateField()),
                (
                    "created_at",
                    models.DateTimeField(
                        default=datetime.datetime(2014, 9, 7, 18, 0, 27, 580872),
                        auto_now_add=True,
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        default=datetime.datetime(2014, 9, 7, 18, 0, 27, 580896),
                        auto_now=True,
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        to="categories.Category",
                        null=True,
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "ordering": ["-date"],
            },
            bases=(models.Model,),
        ),
    ]
