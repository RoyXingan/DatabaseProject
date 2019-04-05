from django.contrib import admin
from .models import Model
# Register your models here.


class ModelAdmin(admin.ModelAdmin):
    # fields = ["model_title",
    #           "model_published",
    #           "model_content"]

    fieldsets = [
        ("Title/date", {"fields": ["model_title", "model_published"]}),
        ("Content", {"fields": ["model_content"]})
    ]


admin.site.register(Model, ModelAdmin)
