# -*- coding: utf-8 -*-
import datetime
import ImageOps
import os
from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from south.modelsinspector import add_introspection_rules
from apps.utils.fields import upload_path, ImageWithThumbsField
from managers import BlogPostManager
from listeners import render_content

class BlogPost(models.Model):
    _IMG = None
    _GREYSCALE_PATH = None
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
    slug = models.SlugField('URL', help_text="numbers, letters and dashes only.", max_length=255, unique=True)
    description = models.CharField(max_length=255)
    content = models.TextField()
    content_rendered = models.TextField(blank=True, null=True)
    created = models.DateTimeField(default=datetime.datetime.now)
    modified = models.DateTimeField(auto_now=True)
    status = models.PositiveSmallIntegerField('This post is...', default = 0, choices = STATUS_CHOICES)
    views = models.IntegerField(default=0)
    
    objects = BlogPostManager()
    tags = TaggableManager()
    
    def __unicode__(self):
        return u'%s' % self.title
    
    
    @models.permalink
    def get_absolute_url(self):
        return ('posts:show', (), {
            'slug' : self.slug
        } ) 
        
        
    def img(self):
        try:
            self._IMG = self.blogimage_set.all()[0]
        except IndexError:
            return BlankImg()
        return self._IMG
    

class BlankImg(object):
    t = '%simages/blank.t.png' % settings.MEDIA_URL
    l = '%simages/blank.l.png' % settings.MEDIA_URL
    f = '%simages/blank.f.png' % settings.MEDIA_URL
    title = "Blank Image"
    


class BlogImage(models.Model):
    src = ImageWithThumbsField('Image', upload_to=upload_path, sizes=settings.IMAGE_SIZES)
    title = models.CharField(max_length=255, blank=True, null=True)
    blogpost = models.ForeignKey(BlogPost)
    order = models.PositiveSmallIntegerField(default=5)
    
    @property
    def t(self):
        try:
            return self.src.url_200x200
        except AttributeError:
            return False
    
    @property
    def m(self):
        try:
            return self.src.url_320x240
        except AttributeError:
            return False
    
    @property
    def l(self):
        try:
            return self.src.url_612x450
        except AttributeError:
            return False    
    
    @property
    def f(self):
        try:
            return self.src.url_850x600
        except AttributeError:
            return False
    

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


models.signals.pre_save.connect(render_content, sender=BlogPost)