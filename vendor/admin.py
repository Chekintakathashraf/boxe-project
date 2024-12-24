from django.contrib import admin
from .models import *

class SequenceInline(admin.TabularInline):
    model = Sequence
    extra = 1  

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('id', 'vendor_name', 'email', 'address')
    search_fields = ('vendor_name', 'email')
    inlines = [SequenceInline]

@admin.register(Sequence)
class SequenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'alpha', 'numeric', 'padding', 'vendor')
    list_filter = ('type', 'vendor')
    search_fields = ('alpha', 'vendor__vendor_name')
