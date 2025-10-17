from django.db import models
from tinymce.models import HTMLField
from django_resized import ResizedImageField
from django.contrib import admin
from django.db.models.signals import post_delete
from django.dispatch import receiver

class PageContent(models.Model):
    HOME = "HOME"
    ABOUT = "ABOUT"
    CONTACT = "CONTACT"
    TEST = "TEST"
    CHOICES = (
        (HOME, "Home"),
        (ABOUT, "About"),
        (CONTACT, "Contact"),
        (TEST, "Test")
    )
    page = models.CharField(max_length=8, null=False, unique=True, choices=CHOICES)
    heading = models.CharField(max_length=64, default="Content Page")
    content = HTMLField()
    
    def __str__(self):
        return self.page

@admin.display(
    ordering='position',
)
class CarouselItem(models.Model):
    position = models.IntegerField(unique=True)
    background_image = ResizedImageField(size=[1920, 1080], upload_to="images/hompage-carousel/", null=False)
    heading = models.CharField(max_length=64)
    content = models.TextField(max_length=300)
    link = models.URLField(max_length=500, blank=True, null=True)
    button_text = models.CharField(max_length=64, default="Read More")
    visible = models.BooleanField(default=False)

    def __str__(self):
        return f"(#{self.position}) {self.heading}"
    
@receiver(post_delete, sender=CarouselItem)
def delete_image_hook(sender, instance, using, **kwargs):
    instance.background_image.delete()
        