from django.contrib import admin
from django.conf import settings
from django.utils.safestring import mark_safe
from django.template.defaultfilters import linebreaksbr

from dashboard.common.db_util import canvas_id_to_incremented_id
from .models import CourseViewOption, Course

from django.forms.models import BaseInlineFormSet, ModelForm

# Always save the OneToOne Fields
# https://stackoverflow.com/a/3734700/3708872
class AlwaysChangedModelForm(ModelForm):
    def has_changed(self, *args, **kwargs):
        if self.instance.pk is None:
            return True
        return super(AlwaysChangedModelForm, self).has_changed(*args, **kwargs)

class CourseInline(admin.TabularInline):
    model = Course

class CourseViewOptionInline(admin.StackedInline):
    model = CourseViewOption
    form = AlwaysChangedModelForm

    exclude = ()

    # exclude disabled views
    for view in CourseViewOption.VIEWS:
        if view in settings.VIEWS_DISABLED:
            exclude += (view,)

class CourseAdmin(admin.ModelAdmin):
    inlines = [CourseViewOptionInline,]
    list_display = ('name', 'term_id','_courseviewoption')
    list_select_related = True

    # Need this method to correctly display the line breaks
    def _courseviewoption(self, obj):
        return mark_safe(linebreaksbr(obj.courseviewoption))
    _courseviewoption.short_description = "Course View Option(s)"

    # When saving the course, update the id based on canvas id
    def save_model(self, request, obj, form, change):
        obj.id = canvas_id_to_incremented_id(obj.canvas_id)
        return super(CourseAdmin, self).save_model(request, obj, form, change)
        
admin.site.register (Course, CourseAdmin)