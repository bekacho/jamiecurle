from django.db import models
from managers import VisitManager


class Script(models.Model):
    path = models.TextField()
    
    def __unicode__(self):
        return u'%s' % self.path
    


class Spider(models.Model):
    identifier = models.CharField( max_length=255, unique=True)
    disallow = models.BooleanField(default=False)
    def __unicode__(self):
        return self.identifier
    
    

class Visit(models.Model):
    HUMAN = 1
    SPIDER = 2
    SCRIPT = 3
    STATUS_CHOICES = (
        (HUMAN, 'Human'),
        (SPIDER, 'Spider'),
        (SCRIPT, 'Script'),
    )
    http_referer = models.TextField( blank=True, null=True )
    path_info = models.TextField( blank=True, null=True )
    remote_addr = models.IPAddressField( blank=True, null=True )
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    sessionid = models.CharField( max_length=255, blank=True, null=True )
    user_agent = models.CharField( max_length=255, blank=True, null=True )
    created = models.DateTimeField( auto_now_add=True)
    
    
    objects = VisitManager()
    
    def __unicode__(self):
        return u'%s' % self.created
    
    def short_user_agent(self):
        try:
            return '%s...' % self.user_agent[:50]
        except TypeError:
            return ''
    
    def search_queries(self):
        return ''.join( [q.value for q in self.querystringparameter_set.filter(key="q")] )
    
    def short_referer(self):
        try:
            return self.http_referer[:30]
        except TypeError:
            return ''
    



class QuerystringParameter(models.Model):
    visit = models.ForeignKey(Visit)
    key = models.CharField(max_length=255)
    value = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return self.key
    
