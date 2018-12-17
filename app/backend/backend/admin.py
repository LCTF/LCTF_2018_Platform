# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

class ChallengesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'author', 'flag', 'show', )
    search_fields = ('name', )

class HintsAdmin(admin.ModelAdmin):
    list_display = ('chal', 'content', 'date', )
    search_fields = ('content', )

class TeamsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'school', )
    search_fields = ('name', )

class SolvesAdmin(admin.ModelAdmin):
    list_display = ('chal', 'team', 'ip', 'date', )

class WrongKeysAdmin(admin.ModelAdmin):
    list_display = ('chal', 'team', 'flag', 'ip', 'date', )
    search_fields = ('flag', )

class NoticesAdmin(admin.ModelAdmin):
    list_display = ('content', 'date', )
    search_fields = ('content', )

class ConfigAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'official_avatar', )

class AuthorsAdmin(admin.ModelAdmin):
    list_display = ('name', 'avatar', )

class IndexAdmin(admin.ModelAdmin):
    list_display = ('content', )

admin.site.register(Challenges, ChallengesAdmin)
admin.site.register(Hints, HintsAdmin)
admin.site.register(Teams, TeamsAdmin)
admin.site.register(Solves, SolvesAdmin)
admin.site.register(Wrong_keys, WrongKeysAdmin)
admin.site.register(Notices, NoticesAdmin)
admin.site.register(Config, ConfigAdmin)
admin.site.register(Authors, AuthorsAdmin)
admin.site.register(Index, IndexAdmin)

