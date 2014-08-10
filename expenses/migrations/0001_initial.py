# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Expense'
        db.create_table(u'expenses_expense', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('payment', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categories.Category'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 5, 0, 0), auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 5, 0, 0), auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'expenses', ['Expense'])


    def backwards(self, orm):
        # Deleting model 'Expense'
        db.delete_table(u'expenses_expense')


    models = {
        u'categories.category': {
            'Meta': {'object_name': 'Category'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 5, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 5, 0, 0)', 'auto_now': 'True', 'blank': 'True'})
        },
        u'expenses.expense': {
            'Meta': {'object_name': 'Expense'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categories.Category']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 5, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 5, 0, 0)', 'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['expenses']