from django.db import models
from apps import assets
from tagging.fields import TagField

class Page(models.Model):
    IMG_CACHE = False
    HIDDEN = 1
    DRAFT = 2
    PUBLISHED = 3
        
    STATUS_CHOICES  = (
        (HIDDEN, 'Hidden'),
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    content = models.TextField()
    tags = TagField()
    status = models.SmallIntegerField(default=DRAFT, choices=STATUS_CHOICES)
    sticky = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    comments = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return u'%s' % self.pk
    
    @models.permalink
    def get_absolute_url(self):
        return ('info_page', (self.slug,))

assets.register(Page)