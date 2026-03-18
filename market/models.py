import uuid
from decimal import Decimal
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

#choice sets for model fields
ITEM_CATEGORY_CHOICES = (
    ("FURNITURE", "Furniture"),
    ("ELECTRONICS", "Electronics"),
    ("CLOTHING", "Clothing"),
    ("STATIONERY", "Stationery"),
    ("BOOKS", "Books"),
    ("SPORTS", "Sports"),
    ("OTHER", "Other"),
)

ITEM_STATUS_CHOICES = (
    ("AVAILABLE", "Available"),
    ("SOLD", "Sold"),
)

TRANSACTION_TYPE_CHOICES = (
    ("PURCHASE", "Purchase"),
    ("TOPUP", "Topup"),
)

#words that can't appear in the title or description
PROHIBITED_KEYWORDS = (
    "food", "drink", "beverage", "pet", "illegal", "prohibited"
)

#validator = prevents users from listing banned items by scanning for prohibited keywords
def validate_not_prohibited(text: str):
    if not text:
        return
    lower = text.lower()
    for word in PROHIBITED_KEYWORDS:
        if word in lower:
            raise ValidationError("This listing appears to include prohibited items. Please revise")

#item model 
class Item(models.Model):
    itemID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # primary key
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="items_listed")

    title = models.CharField(max_length=256, validators=[validate_not_prohibited])
    # Added so clean() reference is valid and to allow scanning both fields.
    description = models.TextField(blank=True, default='')

    category = models.CharField(
        max_length=32,
        choices=ITEM_CATEGORY_CHOICES,
        default="OTHER",
        db_index=True,
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))], #price cant be negative
    )

    status = models.CharField(
        max_length=16,
        choices=ITEM_STATUS_CHOICES,
        default="AVAILABLE",
        db_index=True,
    )
    
    thumbnail = models.ImageField(
        upload_to="thumbnails/",
        blank=True,
        null=True
    )
    
    listed_at = models.DateTimeField(auto_now_add=True) #timestamp autoset on creation

    class Meta:
        #extra indexes for filtering and sorting
        indexes = [
            models.Index(fields=["category", "status"]),
            models.Index(fields=["listed_at"]),
        ]

    def clean(self):
        # Validate combined content for prohibited words
        validate_not_prohibited(f"{self.title} {self.description or ''}")

    def __str__(self):
        return self.title

#item photo model
class ItemPhoto(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="photos"
    )

    image = models.ImageField(upload_to="item_photos/")
    caption = models.CharField(max_length=255, blank=True)

#transaction model
class Transaction(models.Model):
    transactionID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # primary key
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    item = models.ForeignKey(
        Item,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )

    type = models.CharField(max_length=16, choices=TRANSACTION_TYPE_CHOICES, db_index=True)
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def clean(self):
        # Compare against the string values 
        if self.type == "PURCHASE" and self.item is None:
            raise ValidationError("Purchase transactions must reference an item")
        if self.type == "TOPUP" and self.item is not None:
            raise ValidationError("Top-up transactions must not reference an item")

    def __str__(self):
        return f"{self.type} {self.amount} by {self.buyer}"
    

#custom user with UUID primary key and fields from specification
class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #primary key
    username = None #using email instead
    first_name = models.CharField(max_length=128, blank=True)
    last_name = models.CharField(max_length=128, blank=True)

    email = models.EmailField(max_length=256, unique=True)
    student_id = models.CharField(max_length=32, unique=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics/",
        blank=True,
        null=True
    )
    #simulated currency balance
    account_balance = models.DecimalField(max_digits=12, decimal_places=2,default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0.00"))])

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "student_id"]

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"