from django.contrib import admin

from apps.course.models import (Category, Course, Instructor, Lesson, Module,
                                SubCategory, TextLesson, Topic, VideoLesson)


class InstructorAdmin(admin.ModelAdmin):
    readonly_fields = ("total_course_taught",)


class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("view_time",)


class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class ModuleAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": (
            "course",
            "name",
        )
    }
    readonly_fields = ("view_time",)


class LessonAdmin(admin.ModelAdmin):
    pass


class TextLessonAdmin(admin.ModelAdmin):
    pass


class VideoLessonAdmin(admin.ModelAdmin):
    readonly_fields = ("view_time",)


admin.site.register(Course, CourseAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(TextLesson, TextLessonAdmin)
admin.site.register(VideoLesson, VideoLessonAdmin)
