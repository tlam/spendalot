# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'categories_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 5, 0, 0), auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 5, 0, 0), auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'categories', ['Category'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'categories_category')


    models = {
        u'categories.category': {
            'Meta': {'object_name': 'Category'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 5, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 5, 0, 0)', 'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['categories']