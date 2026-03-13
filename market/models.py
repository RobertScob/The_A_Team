import uuid
from decimal import Decimal
from django.db import models
from django.conf import settings 
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

User = settings.AUTH_USER_MODEL

class ItemCategory(models.TextChoices):
    FURNITURE = "FURNITURE", "Furniture"
    ELECTRONICS = "ELECTRONICS", "Electronics"
    CLOTHING = "CLOTHING", "Clothing"
    STATIONERY = "STATIONERY", "Stationery"
    BOOKS = "BOOKS", "Books"
    SPORTS = "SPORTS", "Sports"
    OTHER = "OTHER", "Other"

class ItemStatus(models.TextChoices):
    AVAILABLE = "AVAILABLE", "Available"
    SOLD = "SOLD", "Sold"

class TransactionType(models.TextChoices):
    PURCHASE = "PURCHASE", "Purchase"
    TOPUP = "TOPUP", "Topup"

PROHIBITED_KEYWORDS = (
    "food", "drink", "beverage", "pet", "illegal", "prohibited"
)

def vaalidate_not_prohibited(text:str):
    if not text:
        return
    lower = text.lower()
    for word in PROHIBITED_KEYWORDS:
        if word in lower:
            raise ValidationError("This listing appears to include prohibited items. Please revise")
        
class Item(models.Model):
    itemID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #primary key
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items_listed")

    title = models.CharField(max_length=256, validators=[vaalidate_not_prohibited])

    category = models.CharField(max_length=32, 
                                choices=ItemCategory.choices,
                                default=ItemCategory.other,
                                db_index=True,)
    
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])

    status = models.CharField(max_length=16, choices=ItemStatus.choicrs, default=ItemStatus.AVAILABLE, db_index=True)
    listed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["category", "status"]),
            models.Index(fields=["listed_at"])
        ]

    def clean(self):
        vaalidate_not_prohibited(f"{self.title}{self.description or ''}")

    def __str__(self):
        return self.title
    
class ItemPhoto(models.Model):
    photoID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #prikary key
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="photos")
    url = models.CharField(max_length=512)
    caption = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return f"Photo for {self.itemID}"
    

class Transaction(models.Model):
    transactionID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #primary key
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True,related_name='transactions')

    type = models.CharField(max_length=16, choices=TransactionType.choices, db_index=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])
    date = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = ["-date"]

    def clean(self):
        if self.type == TransactionType.PURCHASE and self.item is None:
            raise ValidationError("Purchase transactions must reference an item")
        if self.type == TransactionType.TOPUP and self.item is not None:
            raise ValidationError("Top-up transactions must not reference an item")
        
    def __str__(self):
        return f"{self.type} {self.amount} by {self.buyer}"
    
    