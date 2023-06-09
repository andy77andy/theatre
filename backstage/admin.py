from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Actor


@admin.register(Actor)
class ActorAdmin(UserAdmin):
    pass
    # list_display = UserAdmin.list_display + ("average_fee", "awards",)
    # fieldsets = UserAdmin.fieldsets + (
    #     (("Additional info", {"fields": ("average_fee", "awards",)}),)
    # )
    #
    # add_fieldsets = UserAdmin.add_fieldsets + (
    #     (
    #         (
    #             "Additional info",
    #             {
    #                 "fields": (
    #                     "email",
    #                     "first_name",
    #                     "last_name",
    #                     "average_fee",
    #                     "awards",
    #                 )
    #             },
    #         ),
    #     )
    # )


# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     search_fields = ("title",)
#
#
# @admin.register(Commentary)
# class CommentaryAdmin(admin.ModelAdmin):
#     search_fields = ("post",)
#     list_filter = ("created_time",)
# from django.contrib import admin
#
# # Register your models here.
