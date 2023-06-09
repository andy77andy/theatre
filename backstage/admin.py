from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Actor, Award, Director, Play, Genre


@admin.register(Actor)
class ActorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("average_fee", )
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("average_fee", "awards",)}),)
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "email",
                        "first_name",
                        "last_name",
                        "average_fee",
                        "awards",
                    )
                },
            ),
        )
    )


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_filter = ("year",)


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    search_fields = ("last_name",)


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    search_fields = ("name",)
#
#
# @admin.register(Genre)
# class PlayAdmin(admin.ModelAdmin):
#     pass
