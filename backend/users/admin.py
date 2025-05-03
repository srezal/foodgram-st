from django.contrib import admin
from .models import User, Subscription


admin.site.register(
    [Subscription]
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('username', 'email')
    search_help_text = 'Поиск по username или email'