from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver 
from django.core.exceptions import ValidationError
from .models import Transaction, TransactionType, ItemStatus

@receiver(post_save, sender=Transaction)
def handle_transaction(sender, instance: Transaction, created, **kwargs):
    if not created:
        return
    buyer = instance.buyer

    if instance.type == TransactionType.TOPUP:
        buyer.account_balance += instance.amount
        buyer.save(update_fields=["account_balance"])
        return
    
    item = instance.item
    if item is None:
        raise ValidationError("Purchase must have an item")
    
    if item.status == ItemStatus.SOLD:
        raise ValidationError("Item already sold")
    
    if buyer.account_balance < instance.amount:
        raise ValidationError("Insufficient balance")
    
    seller = item.seller
    buyer.account_balance -= instance.amount
    seller.account_balance += instance.amount
    buyer.save(update_fields=["account_balance"])
    seller.save(update_fields=["account_balance"])

    item.status = ItemStatus.SOLD
    item.save(update_fields=["status"])

    