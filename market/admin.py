from django.contrib import admin
from .models import Item, ItemPhoto, Transaction
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User

#inline admin to allow adding/editting photos of items directly, within the item admin page
class ItemPhotoInline(admin.TabularInline):
    model = ItemPhoto
    extra = 1

#admin configuration for item model
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    #fields shown in admin list view
    list_display = ("title", "seller","category", "price", "status", "listed_at")
    list_filter = ("category", "status") #sidebar filters
    search_fields = ("title", "description") #searchable fields
    inlines = [ItemPhotoInline] #allow inline management of item photos

#admin config for transaction moddel
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("type", "buyer", "item", "amount", "date")
    list_filter = ("type", )
    search_fields = ("buyer__email", "item__title")

#user admin which extends builtin UserAdmin
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    list_display = ("email", "first_name", "last_name", "student_id", "account_balance", "is_staff")
    ordering = ("email", )
    search_fields = ("email", "student_id", "first_name", "last_name")
    
    #field sections for user detail page
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "student_id", "profile_picture", "account_balance")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    
    #fields shown when creating new user through admin site
    add_fieldsets = (
        (None, {"classes": ("wide",),
                "fields": ("email", "first_name", "last_name", "student_id", "password1", "password2")}),
    )
