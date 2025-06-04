import nested_admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import OTPRequest, User, PhoneNumber


admin.site.site_header = "OYSIRS Administration"
admin.site.site_title = "OYSIRS Administration"
admin.site.index_title = "Welcome to OYSIRS Admin Dashboard"


class PhoneNumberInline(nested_admin.NestedTabularInline):
    model = PhoneNumber
    extra = 0
    max_num = 1


@admin.register(User)
class UserAdmin(BaseUserAdmin, nested_admin.NestedModelAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "email_verified",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "first_name", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)
    inlines = [PhoneNumberInline]


@admin.register(OTPRequest)
class OTPRequestAdmin(nested_admin.NestedModelAdmin):
    list_display = ("ref", "otp", "is_verified", "has_expired", "created_at")
    search_fields = ("ref",)
    ordering = ("-created_at",)
    list_filter = ("created_at",)