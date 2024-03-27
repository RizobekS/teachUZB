from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class HomePageAbout1(models.Model):
    subtitle = RichTextUploadingField()

    def __str__(self):
        return self.subtitle

    class Meta:
        verbose_name = "Home Page About 1"
        verbose_name_plural = "Home Page About 1"


class Section1(models.Model):
    parent = models.ForeignKey(HomePageAbout1, on_delete=models.CASCADE)
    title = models.CharField(max_length=600)
    subtitle = models.TextField(max_length=2000)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Section 1"
        verbose_name_plural = "Section 1"


class HomePageAbout2(models.Model):
    subtitle = RichTextUploadingField()

    def __str__(self):
        return self.subtitle

    class Meta:
        verbose_name = "Home Page About 2"
        verbose_name_plural = "Home Page About 2"


class Section2(models.Model):
    parent = models.ForeignKey(HomePageAbout2, on_delete=models.CASCADE)
    title = models.CharField(max_length=600)
    subtitle = models.TextField(max_length=2000)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Section 2"
        verbose_name_plural = "Section 2"
