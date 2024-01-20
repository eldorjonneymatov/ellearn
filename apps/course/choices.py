from django.db import models
from django.utils.translation import gettext_lazy as _

class CourseStatusChoices(models.TextChoices):
    DRAFT = 'draft', _('Draft')
    PUBLISHED = 'published', _('Published')
    HIDDEN = 'hidden', _('Hidden')


class LanguageChoices(models.TextChoices):
    ENGLISH = 'en', _('English')
    UZBEK = 'uz', _('Uzbek')
    RUSSIAN = 'ru', _('Russian')
    TADJIK = 'tg', _('Tadjik')
    KAZAKH = 'kk', _('Kazakh')
    KRGYZ = 'ky', _('Krgyz')
    ARABIC = 'ar', _('Arabic')
    CHINESE = 'zh', _('Chinese')
    FRENCH = 'fr', _('French')
    GERMAN = 'de', _('German')
    HINDI = 'hi', _('Hindi')
    ITALIAN = 'it', _('Italian')
    JAPANESE = 'ja', _('Japanese')
    KOREAN = 'ko', _('Korean')
    PORTUGUESE = 'pt', _('Portuguese')
    SPANISH = 'es', _('Spanish')
    TURKISH = 'tr', _('Turkish')
    OTHER = 'other', _('Other')