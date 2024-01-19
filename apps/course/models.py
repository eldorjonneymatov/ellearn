from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from django.core.validators import FileExtensionValidator

from apps.core.models import TimeStampedModel
from apps.course.choices import CourseStatusChoices
from apps.course.managers import PublishedManager

class CourseAuthor(TimeStampedModel):
    pass

class Category(TimeStampedModel):
    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=255, unique=True)

    class Meta:
        db_table = 'course_categories'
        verbose_name = _('Course Category')
        verbose_name_plural = _('Course Categories')
        ordering = ('name',)

    def __str__(self):
        return self.name
    

class SubCategory(TimeStampedModel):
    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=255, unique=True)
    category = models.ForeignKey(
        Category, verbose_name=_('Category'), related_name='subcategories', on_delete=models.PROTECT
    )

    class Meta:
        db_table = 'course_subcategories'
        verbose_name = _('Course SubCategory')
        verbose_name_plural = _('Course SubCategories')
        ordering = ('name',)

    def __str__(self):
        return self.name
    

class Course(TimeStampedModel):
    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=255, unique=True)
    description = models.TextField(_('Description'))
    is_free = models.BooleanField(_('Is Free?'), default=False)
    author = models.ForeignKey(
        CourseAuthor, verbose_name=_('Author'), related_name='courses', on_delete=models.PROTECT
    )
    cover_image = ResizedImageField(
        _('Cover Image'), size=[1080, 566], crop=['middle', 'center'], quality=90, upload_to="course/cover_images"
    )
    subcategory = models.ForeignKey(
        SubCategory, verbose_name=_('SubCategory'), related_name='courses', on_delete=models.PROTECT
    )
    certificate_file = models.FileField(
        _('Certificate File'), upload_to='course/certificate_files', blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['html'])]
    )
    status = models.CharField(
        _('Status'), max_length=20, choices=CourseStatusChoices.choices, default=CourseStatusChoices.DRAFT
    )

    objects = models.Manager()
    published = PublishedManager()
    
    @property
    def has_certificate(self):
        return self.certificate_file is not None
    
    class Meta:
        db_table = 'courses'
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')
        ordering = ('name',)

    def __str__(self):
        return self.name