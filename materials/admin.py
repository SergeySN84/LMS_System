from django.contrib import admin
from .models import Course, Lesson


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ("title", "description", "video_url", "preview", "owner")
    readonly_fields = ("owner",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "lessons_count")
    list_filter = ("owner",)
    search_fields = ("title", "description", "owner__email")
    inlines = [LessonInline]

    def lessons_count(self, obj):
        return obj.lessons.count()

    lessons_count.short_description = "Кол-во уроков"


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "owner", "video_url")
    list_filter = ("course", "owner")
    search_fields = ("title", "description", "course__title", "owner__email")
    autocomplete_fields = ["course", "owner"]
