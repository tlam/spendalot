from django.db import models


class Keyword(models.Model):
    words = models.CharField(max_length=200)
    category = models.ForeignKey('categories.Category')

    def __unicode__(self):
        return u'{}'.format(self.words)
