# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding M2M table for field scripts on 'Page'
        db.create_table('info_page_scripts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_page', models.ForeignKey(orm['info.page'], null=False)),
            ('to_page', models.ForeignKey(orm['info.page'], null=False))
        ))
        db.create_unique('info_page_scripts', ['from_page_id', 'to_page_id'])


    def backwards(self, orm):
        
        # Removing M2M table for field scripts on 'Page'
        db.delete_table('info_page_scripts')


    models = {
        'info.page': {
            'Meta': {'object_name': 'Page'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['info.Page']", 'null': 'True', 'blank': 'True'}),
            'scripts': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'frank'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['info.Page']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['info']
