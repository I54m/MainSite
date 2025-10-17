from django.db import models
from tinymce.models import HTMLField
from django_resized import ResizedImageField
from django.utils import timezone
from django.contrib import admin
from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver

import os

@admin.display(
    ordering='position',
)
class Category(models.Model):
    name = models.CharField(max_length=100)
    position = models.IntegerField(unique=True)
    summary = models.TextField(max_length=300, null=True)
    visible = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        # if the category does not have any visible projects associated with it then set the category invisible
        if self.project_set.filter(visible=True).count() == 0 and self.visible:
            self.visible = False
        super().save()

def file_path(self, filename):
    ext = filename.split('.')[-1]
    filename = f"{self.slug}.{ext}"
    path = "images/projects/thumbnails/"
    return os.path.join(path, filename)

@admin.display(
    ordering='start_date',
)
class Project(models.Model):
    slug = models.SlugField(unique=True, null=False) # autofilled on the admin page
    title = models.CharField(max_length=32, null=False)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1)
    thumbnail = ResizedImageField(size=[512, 512], default="images/default-project.png", upload_to=file_path)
    summary = models.TextField(max_length=200, default="Default project summary")
    description = HTMLField()
    technology = models.CharField(max_length=32, null=False)
    start_date = models.DateField(default=timezone.now, null=False)
    visible = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    #optional urls and links
    github_url = models.URLField(max_length=500, blank=True)
    jenkins_url = models.URLField(max_length=500, blank=True)
    demo_url = models.URLField(max_length=500, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save()
        # if the projects category does not have any visible projects associated with it then set the category invisible
        category = Category.objects.get(pk=self.category.pk)
        if category.project_set.filter(visible=True).count() == 0:
            category.visible = False
            category.save()

@receiver(pre_delete, sender=Project)
def pre_delete_project_hook(sender, instance, using, **kwargs):
    for gallery in instance.gallery_set.all():
        gallery.delete()
        gallery.image.delete()

@receiver(post_delete, sender=Project)
def post_delete_project_hook(sender, instance, using, **kwargs):
    if instance.thumbnail.name != "images/default-project.png":  
        instance.thumbnail.delete()
    
# project gallery images shown in a carousel on detail page
class Gallery(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = ResizedImageField(size=[1920, 1080], upload_to="images/projects/gallery_images/")

    def __str__(self):
        return "Gallery Image"
        
# project credit shown on the detail to credit developers for their source code used etc
class Credit(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    person = models.CharField(max_length=32, null=False)
    credited_for = models.CharField(max_length=32, null=False)
    
    def __str__(self):
        return f"{self.person} - {self.credited_for}"