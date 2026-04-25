
# Register your models here.

from django.contrib import admin
from .models import Resume, Skill, UserSkill

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill', 'created_at']
    search_fields = ['user__username', 'skill__name']


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']