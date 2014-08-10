# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Keyword'
        db.create_table(u'keywords_keyword', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('words', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['categories.Category'])),
        ))
        db.send_create_signal(u'keywords', ['Keyword'])


    def backwards(self, orm):
        # Deleting model 'Keyword'
        db.delete_table(u'keywords_keyword')


    models = {
        u'categories.category': {
            'Meta': {'object_name': 'Category'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 5, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 5, 0, 0)', 'auto_now': 'True', 'blank': 'True'})
        },
        u'keywords.keyword': {
            'Meta': {'object_name': 'Keyword'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['categories.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'words': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['keywords']