from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from django.core.validators import FileExtensionValidator
from djrichtextfield.models import RichTextField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError

from apps.common.models import TimeStampedModel
from apps.course.choices import (
    CourseStatusChoices, LanguageChoices
)
from apps.course.managers import PublishedManager
from apps.common.utils import (
    calculate_reading_time, get_video_length
)


class Instructor(TimeStampedModel):
    full_name = models.CharField(_('Full Name'), max_length=255)
    title = models.CharField(_('Title'), max_length=255)
    avatar = ResizedImageField(
        _('Avatar'), size=[240, 240], crop=['middle', 'center'], quality=90, upload_to="course/instructor/avatars"
    )
    description = models.TextField(_('Description'))
    website = models.URLField(_('Website'), blank=True, null=True)
    facebook = models.URLField(_('Facebook'), blank=True, null=True)
    twitter = models.URLField(_('Twitter'), blank=True, null=True)
    linkedin = models.URLField(_('Linkedin'), blank=True, null=True)
    telegram = models.URLField(_('Telegram'), blank=True, null=True)

    class Meta:
        db_table = 'course_instructors'
        verbose_name = _('Course Instructor')
        verbose_name_plural = _('Course Instructors')
        ordering = ('full_name',)

    def __str__(self):
        return self.full_name


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
    

class Topic(TimeStampedModel):
    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=255, unique=True)
    subcategory = models.ForeignKey(
        SubCategory, verbose_name=_('SubCategory'), related_name='topics', on_delete=models.PROTECT
    )

    class Meta:
        db_table = 'course_topics'
        verbose_name = _('Course Topic')
        verbose_name_plural = _('Course Topics')
        ordering = ('name',)

    def __str__(self):
        return self.name
    

class Course(TimeStampedModel):
    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=255, unique=True)
    description = RichTextField(_('Description'))
    is_free = models.BooleanField(_('Is Free?'), default=False)
    instructors = models.ManyToManyField(
        Instructor, verbose_name=_('Instructors'), related_name='courses'
    )
    cover_image = ResizedImageField(
        _('Cover Image'), size=[1080, 566], crop=['middle', 'center'], quality=90, upload_to="course/cover_images"
    )
    topic = models.ForeignKey(
        Topic, verbose_name=_('Topic'), related_name='courses', on_delete=models.PROTECT
    )
    certificate_file = models.FileField(
        _('Certificate File'), upload_to='course/certificate_files', blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['html'])]
    )
    status = models.CharField(
        _('Status'), max_length=20, choices=CourseStatusChoices.choices, default=CourseStatusChoices.DRAFT
    )
    language = models.CharField(
        _('Language'), max_length=10, choices=LanguageChoices.choices, default=LanguageChoices.UZBEK
    )
    view_time = models.DurationField(_('View time in seconds'), default=0)

    objects = models.Manager()
    published = PublishedManager()
    
    def has_certificate(self):
        return self.certificate_file is not None
    
    class Meta:
        db_table = 'courses'
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')
        ordering = ('name',)

    def __str__(self):
        return self.name


class Module(TimeStampedModel):
    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=255, unique=True)
    course = models.ForeignKey(
        Course, verbose_name=_('Course'), related_name='modules', on_delete=models.PROTECT
    )
    description = RichTextField(_('Description'))
    order = models.PositiveIntegerField(_('Order'), default=0)
    view_time = models.DurationField(_('View time in seconds'), default=0)

    def save(self, *args, **kwargs):
        if not self.order:
            self.order = self.course.modules.count() + 1
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'course_modules'
        verbose_name = _('Course Module')
        verbose_name_plural = _('Course Modules')
        ordering = ('order',)

    def __str__(self):
        return self.name
    

class Lesson(TimeStampedModel):
    module = models.ForeignKey(
        Module, verbose_name=_('Module'), related_name='lessons', on_delete=models.PROTECT
    )
    lesson_type = models.ForeignKey(
        ContentType, verbose_name=_('Lesson Type'), related_name='lessons', on_delete=models.PROTECT,
        limit_choices_to={'model__in': ('textlesson', 'videolesson',)}
    ) # add these models in future versions: 'quizlesson', 'resourcelesson', 'assignmentlesson'
    object_id = models.PositiveIntegerField(_('Object ID'))
    item = GenericForeignKey('lesson_type', 'object_id')
    description = models.CharField(_('Description'))
    order = models.PositiveIntegerField(_('Order'), default=0)

    def save(self, *args, **kwargs):
        if not self.order:
            self.order = self.module.lessons.count() + 1
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'course_lessons'
        verbose_name = _('Course Lesson')
        verbose_name_plural = _('Course Lessons')
        ordering = ('order',)


class LessonBase(TimeStampedModel):
    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=255, unique=True)
    description = RichTextField(_('Description'))
    order = models.PositiveIntegerField(_('Order'), default=0)
    view_time = models.DurationField(_('View time in seconds'))

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.order:
            self.order = self.module.lessons.count() + 1
        new_view_time = self.process_view_time()
        if new_view_time > 0:
            self.update_ancestor_view_times(new_view_time)
        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        self.update_ancestor_view_times(-self.view_time)
        super().delete(*args, **kwargs)

    def process_view_time(self):
        raise NotImplementedError

    def update_ancestor_view_times(self, new_view_time):
        self.module.view_time += new_view_time
        self.module.save()
        course = self.module.course
        course.view_time += new_view_time
        course.save()

    def __str__(self):
        return self.name
    

class TextLesson(LessonBase):
    content = RichTextUploadingField(_('Content'))
    
    def process_view_time(self):
        old = TextLesson.objects.filter(pk=self.id)
        if old.exists():
            new_view_time = -old.first().view_time
        else:
            new_view_time = 0
        view_time = calculate_reading_time(self.content) * 60
        new_view_time += view_time
        return new_view_time
    
    class Meta:
        db_table = 'course_text_lessons'
        verbose_name = _('Text Lesson')
        verbose_name_plural = _('Text Lessons')
        ordering = ('order',)


class VideoLesson(LessonBase):
    video = models.FileField(
        _('Video'), upload_to='course/videos',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mkv'])]
    )
    thumbnail = ResizedImageField(
        _('Thumbnail'), size=[1080, 566], crop=['middle', 'center'], quality=90, upload_to="course/thumbnails"
    )

    def process_view_time(self):
        old = VideoLesson.objects.filter(pk=self.id)
        if old.exists():
            path = self.video.file
            new_view_time = -old.first().view_time
        else:
            path = self.video.file.temporary_file_path()
            new_view_time = 0
        view_time = get_video_length(path)
        if view_time is None:
            raise ValidationError({'video': _('Video file is not valid')})
        self.view_time = view_time
        new_view_time += self.view_time
        return new_view_time
    
    class Meta:
        db_table = 'course_video_lessons'
        verbose_name = _('Video Lesson')
        verbose_name_plural = _('Video Lessons')
        ordering = ('order',)
