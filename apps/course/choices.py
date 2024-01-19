from django.db import models
from django.utils.translation import gettext_lazy as _

class CourseStatusChoices(models.TextChoices):
    DRAFT = 'draft', _('Draft')
    PUBLISHED = 'published', _('Published')
    HIDDEN = 'hidden', _('Hidden')