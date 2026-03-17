#population script
import os 
import django 
from decimal import Decimal
import uuid

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "marketplace.settings")
django.setup()

from accounts.models import User
from market.models import Item, ITEM_STATUS_CHOICES, ITEM_CATEGORY_CHOICES, ItemPhoto, Transaction, TRANSACTION_TYPE_CHOICES


def createUser(email, firstname, lastname, student_id, balance):
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            "first_name":firstname,
            "last_name": lastname,
            "student_id": student_id,
            "account_balance": balance, 
        },
    )

    if created:
        user.set_password("123456")
        user.save()
    return user

def populate():
    print("Beginning population")

    #clears old data
    ItemPhoto.objects.all().delete()
    Transaction.objects.all().delete()
    Item.objects.all().delete()
    User.objects.exclude(is_superuser=True).delete()

    #creates users
    tess = createUser("tess@gla.ac.uk", "Tess", "Byrne", "123456", Decimal("50.00"))
    robert = createUser("robert@student.gla.ac.uk", "Robert", "Scobie", "112345", Decimal("0.00"))
    ore = createUser("ore@student.gla.ac.uk", "Ore", "Ajibade", "111234", Decimal("30.00"))

    #creates items
    lamp = Item.objects.create(
        seller=robert,
        title="Desk Lamp",
        description="Bright LED desk lamp",
        category=ITEM_CATEGORY_CHOICES.GADGETS,
        price=Decimal("10.00"),
        status=ITEM_STATUS_CHOICES.AVAILABLE,
    )

    chair = Item.objects.create(
        seller=robert,
        title="Office Chair",
        description="Comfortable black office chair",
        category=ITEM_CATEGORY_CHOICES.FURNITURE,
        price=Decimal("35.00"),
        status=ITEM_STATUS_CHOICES.AVAILABLE,
    )

    
    hoodie = Item.objects.create(
        seller=tess,
        title="Glasgow Uni Hoodie",
        description="Blue hoodie, size M",
        category=ITEM_CATEGORY_CHOICES.CLOTHES,
        price=Decimal("15.00"),
        status=ITEM_STATUS_CHOICES.AVAILABLE,
    )

    
    ItemPhoto.objects.create(item=lamp, url="https://img.freepik.com/premium-photo/white-lamp-with-white-shade-that-says-name-it_1288405-517.jpg", caption="Front view")
    ItemPhoto.objects.create(item=chair, url="https://images.furnituredealer.net/img/products/coaster/color/office%20chairs_800209-b0.jpg", caption="Chair photo")

    #creates transactions  
    # Ore tops up his balance
    Transaction.objects.create(
        buyer=ore,
        type=TRANSACTION_TYPE_CHOICES.TOPUP,
        amount=Decimal("20.00"),
    )

    # Ore buys lamp off of Robert
    Transaction.objects.create(
        buyer=ore,
        type=TRANSACTION_TYPE_CHOICES.PURCHASE,
        amount=Decimal("10.00"),
        item=lamp,
    )

    lamp.status = ITEM_STATUS_CHOICES.SOLD
    lamp.save()

    print("population complete")

if __name__ == "__main__":
    populate()