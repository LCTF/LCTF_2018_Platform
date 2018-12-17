# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Authors(models.Model):
    name = models.CharField(max_length = 80)
    avatar = models.ImageField(upload_to = 'avatar')

    def __str__(self):
        return self.name
   
    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

@python_2_unicode_compatible
class Challenges(models.Model):
    name = models.CharField(max_length = 80)
    description = models.TextField()
    value = models.IntegerField()
    category = models.CharField(max_length = 80)
    bouns = models.CharField(max_length = 80, default = '{"0":0.15,"1":0.1,"2":0.05}')
    flag =  models.TextField()
    author = models.ForeignKey(Authors)
    show = models.BooleanField()

    def __str__(self):
        return self.name
   
    class Meta:
        verbose_name = 'Challenge'
        verbose_name_plural = 'Challenges'

@python_2_unicode_compatible
class Hints(models.Model):
    chal = models.ForeignKey(Challenges)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "Hint"
        verbose_name_plural = "Hints"

@python_2_unicode_compatible
class Teams(models.Model):
    email = models.CharField(max_length = 128)
    password = models.CharField(max_length = 32)
    name = models.CharField(max_length = 128)
    school = models.CharField(max_length = 128)    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'

@python_2_unicode_compatible
class Solves(models.Model):
    chal = models.ForeignKey(Challenges)
    team = models.ForeignKey(Teams)
    date = models.DateTimeField(auto_now_add = True)
    value =  models.IntegerField()
    bouns = models.CharField(max_length = 10)
    ip = models.CharField(max_length = 15)

    def __str__(self):
        return unicode(self.team)
   
    class Meta:
        verbose_name = 'Solve'
        verbose_name_plural = 'Solves'

@python_2_unicode_compatible
class Wrong_keys(models.Model):
    chal = models.ForeignKey(Challenges)
    team = models.ForeignKey(Teams)
    date = models.DateTimeField(auto_now_add = True)
    flag =  models.TextField()
    ip = models.CharField(max_length = 15)

    def __str__(self):
        return unicode(self.team)

    class Meta:
        verbose_name = 'Wrong Key'
        verbose_name_plural = 'Wrong Keys'

@python_2_unicode_compatible
class Notices(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Notice'
        verbose_name_plural = 'Notices'

@python_2_unicode_compatible
class Config(models.Model):
    official_avatar = models.ImageField(upload_to = 'avatar')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return unicode(self.id)

    class Meta:
        verbose_name = 'Config'
        verbose_name_plural = 'Config'

@python_2_unicode_compatible
class Index(models.Model):
    content = models.TextField()

    def __str__(self):
        return unicode(self.id)

    class Meta:
        verbose_name = 'Index'
        verbose_name_plural = 'Index'

class Registers(models.Model):
    ip = models.CharField(max_length = 15)
    time = models.IntegerField()

