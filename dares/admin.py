from django.contrib import admin
from .models import Dare, Category, DifficultyLevel, DareCompletion, DareLike, SiteConfiguration

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active', 'dare_count')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')

@admin.register(DifficultyLevel)
class DifficultyLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'color')
    search_fields = ('name',)

@admin.register(Dare)
class DareAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'college', 'category', 'difficulty', 'status', 'is_featured', 'created_at')
    list_filter = ('status', 'is_approved', 'is_featured', 'category', 'difficulty', 'created_at')
    search_fields = ('title', 'name', 'college', 'dare_text')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('views_count', 'likes_count', 'completions_count', 'created_at', 'updated_at', 'approved_at')

@admin.register(DareCompletion)
class DareCompletionAdmin(admin.ModelAdmin):
    list_display = ('dare', 'completer_name', 'completed_at', 'is_verified')
    list_filter = ('is_verified', 'completed_at')
    search_fields = ('completer_name', 'dare__title')
    actions = ['verify_completion']

    def verify_completion(self, request, queryset):
        queryset.update(is_verified=True)
    verify_completion.short_description = "Mark selected completions as verified"

@admin.register(DareLike)
class DareLikeAdmin(admin.ModelAdmin):
    list_display = ('dare', 'user_email', 'created_at')
    search_fields = ('user_email', 'dare__title')

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'allow_submissions', 'require_approval')