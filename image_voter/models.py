from django.db import models

# Create your models here.

PORTRAIT = 1
LANDSCAPE = 2

class Image(models.Model):
    name_for_display = models.CharField(max_length=50)
    image_filename = models.CharField(max_length=100)
    is_portrait = models.BooleanField(default=False)
    generation = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s: %s" % (self.name_for_display, self.image_filename)


class ImageVote(models.Model):
    image = models.ForeignKey(Image, on_delete=models.PROTECT)
    is_preferred = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s: %s" % (self.image, self.is_preferred)