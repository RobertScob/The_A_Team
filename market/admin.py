from django.contrib import admin
from .models import Item, ItemPhoto, Transaction
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User

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

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    list_display = ("email", "first_name", "last_name", "student_id", "account_balance", "is_staff")
    ordering = ("email", )
    search_fields = ("email", "student_id", "first_name", "last_name")
    
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "student_id", "profile_photo_url", "account_balance")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    
    add_fieldsets = (
        (None, {"classes": ("wide",),
                "fields": ("email", "first_name", "last_name", "student_id", "password1", "password2")}),
    )
