import os
import tempfile

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .. import helpers
from .utils import MEDIA_ENCODING_STATUS, subtitles_file_path


class Language(models.Model):
    """Language model
    to be used with Subtitles
    """

    code = models.CharField(max_length=30, help_text=_("Language code"), verbose_name=_("Code"))

    title = models.CharField(max_length=100, help_text=_("Language name"), verbose_name=_("Title"))

    class Meta:
        ordering = ["id"]
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")

    def __str__(self):
        return f"{self.code}-{self.title}"


class Subtitle(models.Model):
    """Subtitles model"""

    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name=_("Language"))

    media = models.ForeignKey("Media", on_delete=models.CASCADE, related_name="subtitles", verbose_name=_("Media"))

    subtitle_file = models.FileField(
        _("Subtitle/CC file"),
        help_text=_("File has to be WebVTT format"),
        upload_to=subtitles_file_path,
        max_length=500,
    )

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name=_("User"))

    class Meta:
        ordering = ["language__title"]
        verbose_name = _("Subtitle")
        verbose_name_plural = _("Subtitles")

    def __str__(self):
        return f"{self.media.title}-{self.language.title}"

    def get_absolute_url(self):
        return f"{reverse('edit_subtitle')}?id={self.id}"

    @property
    def url(self):
        return self.get_absolute_url()

    def convert_to_srt(self):
        input_path = self.subtitle_file.path
        with tempfile.TemporaryDirectory(dir=settings.TEMP_DIRECTORY) as tmpdirname:
            pysub = settings.PYSUBS_COMMAND

            cmd = [pysub, input_path, "--to", "vtt", "-o", tmpdirname]
            stdout = helpers.run_command(cmd)

            list_of_files = os.listdir(tmpdirname)
            if list_of_files:
                subtitles_file = os.path.join(tmpdirname, list_of_files[0])
                cmd = ["cp", subtitles_file, input_path]
                stdout = helpers.run_command(cmd)  # noqa
            else:
                raise Exception("Could not convert to srt")
        return True


class TranscriptionRequest(models.Model):
    # Whisper transcription request
    media = models.ForeignKey("Media", on_delete=models.CASCADE, related_name="transcriptionrequests", verbose_name=_("Media"))
    add_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Added on"))
    status = models.CharField(
        max_length=20,
        choices=MEDIA_ENCODING_STATUS,
        default="pending",
        db_index=True,
        verbose_name=_("Status"),
    )
    translate_to_english = models.BooleanField(default=False, verbose_name=_("Translate to English"))
    logs = models.TextField(blank=True, null=True, verbose_name=_("Logs"))

    def __str__(self):
        return f"Transcription request for {self.media.title} - {self.status}"

    class Meta:
        verbose_name = _("Transcription request")
        verbose_name_plural = _("Transcription requests")
