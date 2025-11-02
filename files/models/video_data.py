from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .. import helpers


class VideoChapterData(models.Model):
    data = models.JSONField(null=False, blank=False, help_text=_("Chapter data"), verbose_name=_("Chapter data"))
    media = models.ForeignKey(
        'Media',
        on_delete=models.CASCADE,
        related_name='chapters',
        verbose_name=_("Media"),
    )

    class Meta:
        unique_together = ['media']
        verbose_name = _("Video chapter data")
        verbose_name_plural = _("Video chapter data")

    @property
    def chapter_data(self):
        # ensure response is consistent
        data = []
        if self.data and isinstance(self.data, list):
            for item in self.data:
                if item.get("startTime") and item.get("endTime") and item.get("chapterTitle"):
                    chapter_item = {
                        'startTime': item.get("startTime"),
                        'endTime': item.get("endTime"),
                        'chapterTitle': item.get("chapterTitle"),
                    }
                    data.append(chapter_item)
        return data


class VideoTrimRequest(models.Model):
    """Model to handle video trimming requests"""

    VIDEO_TRIM_STATUS = (
        ("initial", _("Initial")),
        ("running", _("Running")),
        ("success", _("Success")),
        ("fail", _("Fail")),
    )

    VIDEO_ACTION_CHOICES = (
        ("replace", _("Replace Original")),
        ("save_new", _("Save as New")),
        ("create_segments", _("Create Segments")),
    )

    TRIM_STYLE_CHOICES = (
        ("no_encoding", _("No Encoding")),
        ("precise", _("Precise")),
    )

    media = models.ForeignKey(
        'Media',
        on_delete=models.CASCADE,
        related_name='trim_requests',
        verbose_name=_("Media"),
    )
    status = models.CharField(
        max_length=20,
        choices=VIDEO_TRIM_STATUS,
        default="initial",
        verbose_name=_("Status"),
    )
    add_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Added on"))
    video_action = models.CharField(
        max_length=20,
        choices=VIDEO_ACTION_CHOICES,
        verbose_name=_("Video action"),
    )
    media_trim_style = models.CharField(
        max_length=20,
        choices=TRIM_STYLE_CHOICES,
        default="no_encoding",
        verbose_name=_("Trim style"),
    )
    timestamps = models.JSONField(
        null=False,
        blank=False,
        help_text=_("Timestamps for trimming"),
        verbose_name=_("Timestamps"),
    )

    def __str__(self):
        return f"Trim request for {self.media.title} ({self.status})"

    class Meta:
        verbose_name = _("Video trim request")
        verbose_name_plural = _("Video trim requests")


@receiver(post_delete, sender=VideoChapterData)
def videochapterdata_delete(sender, instance, **kwargs):
    helpers.rm_dir(instance.media.video_chapters_folder)
