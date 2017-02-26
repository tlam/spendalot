from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return u'{}'.format(self.name)

    def get_absolute_url(self):
        return u'/categories/{}/'.format(self.slug)
