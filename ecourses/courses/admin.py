from django.contrib import admin
from .models import Category, Course, Lesson, Tag
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets \
                        import CKEditorUploadingWidget

class LessonInlineAdmin(admin.StackedInline):
    model = Lesson
    fk_name = 'course'

class LessonTagInlineAdmin(admin.TabularInline):
    model = Lesson.tags.through
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInlineAdmin, ]
    list_display = ['id', 'subject', 'description']
    readonly_fields = ['avatar']
    def avatar(self, obj):
        if obj:
            return mark_safe(
                '<img src="/static/{url}" width="120" />' \
                    .format(url=obj.image.name)
            )
class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Lesson
        fields = '__all__'
class LessonAdmin(admin.ModelAdmin):
    inlines = [LessonTagInlineAdmin, ]
    form = LessonForm
    list_display = ('id', 'subject', 'created_date', 'course')
    list_filter = ('subject', 'created_date')
    search_fields =('subject', 'course__subject')
    readonly_fields = ['avatar']
    def avatar(self, lesson):
        return mark_safe(
            '<img src="/static/{url}" width="120" />'\
                .format(url=lesson.image.name)
        )

    class Media:
        css = {
            'all': ('/static/css/main.css',)
        }

    js = ('/static/js/script.js',)

class TagAdmin(admin.ModelAdmin):
    LessonInlineAdmin = [LessonTagInlineAdmin,]

# Register your models here.
admin.site.register(Category)
admin.site.register(Course, CourseAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Lesson, LessonAdmin)

