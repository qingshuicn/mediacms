from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Page(models.Model):
    slug = models.SlugField(max_length=200, unique=True, verbose_name=_("Slug"))
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    add_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Added on"))
    edit_date = models.DateTimeField(auto_now=True, verbose_name=_("Edited on"))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("get_page", args=[str(self.slug)])

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")


class TinyMCEMedia(models.Model):
    file = models.FileField(upload_to='tinymce_media/', verbose_name=_("File"))
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Uploaded at"))
    file_type = models.CharField(
        max_length=10,
        choices=(
            ('image', _("Image")),
            ('media', _("Media")),
        ),
        verbose_name=_("File type"),
    )
    original_filename = models.CharField(max_length=255, verbose_name=_("Original filename"))
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("User"))

    class Meta:
        verbose_name = _("TinyMCE Media")
        verbose_name_plural = _("TinyMCE Media")
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.original_filename} ({self.file_type})"

    @property
    def url(self):
        return self.file.url
