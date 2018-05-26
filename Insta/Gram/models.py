from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from tinymce.models import HTMLField


# Create your models here.

class tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_photo/')
    Bio = models.CharField(max_length=30)

    def __str__(self):
        return self.user.username

    def delete_profile(self):
        self.delete()


class Image(models.Model):
    image_name = models.CharField(max_length=60)
    image = models.ImageField(upload_to='images/')
    caption = HTMLField()
    editor = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image_name

    def save_editor(self):
        self.save()

    class Meta:
        ordering = ['image']

    def delete_profile(self):
        self.delete()

    def change_profile(self):
        self.change()

    @classmethod
    def todays_images(cls):
        today = dt.date.today()
        images = cls.objects.filter(pub_date__date=today)
        return images

    @classmethod
    def days_news(cls, date):
        images = cls.objects.filter(pub_date__date=date)
        return images

    @classmethod
    def search_by_image_name(cls, search_term):
        images = cls.objects.filter(image_name__icontains=search_term)
        return images
