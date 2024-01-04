from django.contrib import admin
from .models import Category, Exercise, Comment, Profile


# Register your models here.
# admin.site.register(Exercise)

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'category']
    list_display_links = ['pk', 'title']
    list_filter = ['category']


admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Profile)
