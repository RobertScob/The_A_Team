from django.contrib import admin
from .models import Item, ItemPhoto, Transaction

class ItemPhotoInline(admin.TabularInline):
    model = ItemPhoto
    extra = 1

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("title", "seller","category", "price", "status", "listed_at")
    list_filter = ("category", "status")
    search_fields = ("title", "description")
    inlines = [ItemPhotoInline]

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("type", "buyer", "item", "amount", "date")
    list_filter = ("type", )
    search_fields = ("buyer__email", "item__title")

