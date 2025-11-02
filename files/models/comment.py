import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class Comment(MPTTModel):
    """Comments model"""

    add_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Added on"))

    media = models.ForeignKey(
        "Media",
        on_delete=models.CASCADE,
        db_index=True,
        related_name="comments",
        verbose_name=_("Media"),
    )

    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name=_("Parent"),
    )

    text = models.TextField(help_text=_("Text"), verbose_name=_("Text"))

    uid = models.UUIDField(unique=True, default=uuid.uuid4, verbose_name=_("UID"))

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name=_("User"),
    )

    class MPTTMeta:
        order_insertion_by = ["add_date"]

    def __str__(self):
        return f"On {self.media.title} by {self.user.username}"

    def save(self, *args, **kwargs):
        strip_text_items = ["text"]
        for item in strip_text_items:
            setattr(self, item, strip_tags(getattr(self, item, None)))

        if self.text:
            self.text = self.text[: settings.MAX_CHARS_FOR_COMMENT]

        super(Comment, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f"{reverse('get_media')}?m={self.media.friendly_token}"

    @property
    def media_url(self):
        return self.get_absolute_url()

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
