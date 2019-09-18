from django.contrib import admin

from .models import Image, ImageVote


# Register your models here.

admin.site.register(Image)
admin.site.register(ImageVote)
