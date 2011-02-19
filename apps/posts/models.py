# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from south.modelsinspector import add_introspection_rules
from apps.utils.fields import upload_path, ImageWithThumbsField
 
class BlogPost(models.Model):

    HIDDEN = 0
    PUBLISHED = 1
    DELETED = 2
    PRIVATE = 3

    STATUS_CHOICES = (
        (HIDDEN, 'Hidden'),
        (PUBLISHED, 'Published'),
        (DELETED, 'Deleted'),
        (PRIVATE, 'Private'),
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    content = models.TextField()
    content_rendered = models.TextField(blank=True, null=True)
    created = models.DateTimeField(default=datetime.datetime.now)
    modified = models.DateTimeField(auto_now=True)
    status = models.PositiveSmallIntegerField('This post is...', default = 0, choices = STATUS_CHOICES)
    
    def __unicode__(self):
        return u'%s' % self.title
    
    
    @models.permalink
    def get_absolute_url(self):
        return ('posts:post', (self.slug) ) 
    
    

class BlogImage(models.Model):
    src = ImageWithThumbsField('Image', upload_to=upload_path, sizes=settings.IMAGE_SIZES)
    blogpost = models.ForeignKey(BlogPost)
    
    rules = [
        (
            (ImageWithThumbsField, ),
            [],
            {
                "blank": ["blank", {"default": True}],
                "max_length": ["max_length", {"default": 100}],
            },
        ),
    ]
    add_introspection_rules(rules, ["^apps\.utils\.fields",])