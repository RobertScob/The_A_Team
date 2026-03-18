from django.db import transaction
from django.core.exceptions import ValidationError
from decimal import Decimal

def process_purchase(buyer, item):
     if item.status == "SOLD":
          raise ValidationError("Item already sold")

     if buyer.account_balance < item.price:
          raise ValidationError("Insufficient balance")

     seller = item.seller

     with transaction.atomic():
          buyer.account_balance -= item.price
          seller.account_balance += item.price

          buyer.save(update_fields=["account_balance"])
          seller.save(update_fields=["account_balance"])

          item.status = "SOLD"
          item.save(update_fields=["status"])