import uuid
from decimal import Decimal
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

User = settings.AUTH_USER_MODEL

# ----- Choices (2.2-compatible) -----
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

PROHIBITED_KEYWORDS = (
    "food", "drink", "beverage", "pet", "illegal", "prohibited"
)

def validate_not_prohibited(text: str):
    if not text:
        return
    lower = text.lower()
    for word in PROHIBITED_KEYWORDS:
        if word in lower:
            raise ValidationError("This listing appears to include prohibited items. Please revise")

class Item(models.Model):
    itemID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # primary key
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items_listed")

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
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    status = models.CharField(
        max_length=16,
        choices=ITEM_STATUS_CHOICES,
        default="AVAILABLE",
        db_index=True,
    )
    listed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["category", "status"]),
            models.Index(fields=["listed_at"]),
        ]

    def clean(self):
        # Validate combined content for prohibited terms
        validate_not_prohibited(f"{self.title} {self.description or ''}")

    def __str__(self):
        return self.title


class ItemPhoto(models.Model):
    photoID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # primary key
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="photos")
    url = models.CharField(max_length=512)
    caption = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return f"Photo {self.photoID} for {self.item.title}"


class Transaction(models.Model):
    transactionID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # primary key
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
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
        # Compare against the string values used in TRANSACTION_TYPE_CHOICES
        if self.type == "PURCHASE" and self.item is None:
            raise ValidationError("Purchase transactions must reference an item")
        if self.type == "TOPUP" and self.item is not None:
            raise ValidationError("Top-up transactions must not reference an item")

    def __str__(self):
        return f"{self.type} {self.amount} by {self.buyer}"