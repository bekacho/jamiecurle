# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing M2M table for field stylesheets on 'Post'
        db.delete_table('blog_post_stylesheets')

        # Removing M2M table for field scripts on 'Post'
        db.delete_table('blog_post_scripts')

        # Removing M2M table for field images on 'Post'
        db.delete_table('blog_post_images')


    def backwards(self, orm):
        
        # Adding M2M table for field stylesheets on 'Post'
        db.create_table('blog_post_stylesheets', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm['blog.post'], null=False)),
            ('css', models.ForeignKey(orm['assets.css'], null=False))
        ))
        db.create_unique('blog_post_stylesheets', ['post_id', 'css_id'])

        # Adding M2M table for field scripts on 'Post'
        db.create_table('blog_post_scripts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm['blog.post'], null=False)),
            ('js', models.ForeignKey(orm['assets.js'], null=False))
        ))
        db.create_unique('blog_post_scripts', ['post_id', 'js_id'])

        # Adding M2M table for field images on 'Post'
        db.create_table('blog_post_images', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm['blog.post'], null=False)),
            ('img', models.ForeignKey(orm['assets.img'], null=False))
        ))
        db.create_unique('blog_post_images', ['post_id', 'img_id'])


    models = {
        'blog.post': {
            'Meta': {'object_name': 'Post'},
            'comments': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '2'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['blog']
