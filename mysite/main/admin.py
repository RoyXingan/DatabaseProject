from django.contrib import admin
from .models import *


# Register your models here.
# class ModelAdmin(admin.ModelAdmin):
#     # fields = ["model_title",
#     #           "model_published",
#     #           "model_content"]
#
#     fieldsets = [
#         ("Title/date", {"fields": ["model_title", "model_published"]}),
#         ("Content", {"fields": ["model_content"]})
#     ]


admin.site.register(Curriculum)
admin.site.register(Course)
admin.site.register(Topic)
admin.site.register(TopicSet)
admin.site.register(CurriculumCourse)
admin.site.register(Section)
admin.site.register(Goal)
admin.site.register(GradeDistribution)
