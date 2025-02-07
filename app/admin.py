from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app.models import CustomUser, CollectionRequest

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

    # Não inclua o campo 'usable_password' explicitamente
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email', 'first_name', 'last_name', 'driver', 'address', 'neighborhood', 'age', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'driver', 'address', 'neighborhood', 'age', 'phone'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CollectionRequest)