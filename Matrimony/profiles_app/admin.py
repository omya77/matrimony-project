from django.contrib import admin

# Register your models here.

from .models import Religion, Caste, MotherTongue

@admin.register(Religion)
class ReligionAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)

@admin.register(Caste)
class CasteAdmin(admin.ModelAdmin):
    list_display = ('name', 'religion', 'is_active')
    search_fields = ('name', 'religion__name')
    list_filter = ('religion', 'is_active')

@admin.register(MotherTongue)
class MotherTongueAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)

from .models import KYCDocument

@admin.register(KYCDocument)
class KYCDocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_type', 'status', 'submitted_at')
    list_filter = ('status', 'document_type')
    search_fields = ('user__username', 'user__email')
