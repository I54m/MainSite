from django.contrib import admin
from .models import Project, Category, Gallery, Credit

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'visible')
    list_filter = ['position']
    search_fields = ['name']

class ImagesInLine(admin.TabularInline):
    model = Gallery
    extra = 3

class CreditsInLine(admin.TabularInline):
    model = Credit
    extra = 3

class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Project Information', {'fields': ['title', 'category', 'thumbnail', 'technology', 'summary', 'description', 'visible', 'featured']}),
        ('Project Start Date', {'fields': ['start_date'], 'classes': ['collapse']}),
        ('Optional Links', {'fields': ['github_url', 'jenkins_url', 'demo_url'], 'classes': ['collapse']}),
        ('Slug', {'fields': ['slug'], 'classes': ['collapse']}),
    ]
    inlines = [ImagesInLine, CreditsInLine]
    list_display = ('title', 'category', 'technology', 'start_date', 'visible', 'featured')
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ['category']
    search_fields = ['title']

admin.site.register(Project, ProjectAdmin)
admin.site.register(Category, CategoryAdmin)