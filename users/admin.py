# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Payment


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'phone', 'city', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'groups')
    search_fields = ('email', 'phone', 'city')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('phone', 'city', 'avatar')}),
        ('Права', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

admin.site.register(User, CustomUserAdmin)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'lesson', 'amount', 'payment_method', 'payment_date')
    list_filter = ('payment_method', 'payment_date', 'course', 'lesson')
    search_fields = ('user__email', 'course__title', 'lesson__title')
    date_hierarchy = 'payment_date'
    ordering = ('-payment_date',)
