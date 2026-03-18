# populate.py
import os
import django
import random
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "marketplace.settings")
django.setup()

from market.models import (
    User,
    Item,
    ItemPhoto,
    Transaction,
)

# -------------------------
# HELPERS
# -------------------------

def random_image():
    """Return random lorem picsum image"""
    img_id = random.randint(10, 300)
    return f"https://picsum.photos/id/{img_id}/400/300"


def create_user(email, first, last, student_id, balance):
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            "first_name": first,
            "last_name": last,
            "student_id": student_id,
            "account_balance": balance,
        },
    )

    if created:
        user.set_password("123456")
        user.save()

    return user


# -------------------------
# MAIN POPULATION
# -------------------------

def populate():
    print("Clearing database...")

    ItemPhoto.objects.all().delete()
    Transaction.objects.all().delete()
    Item.objects.all().delete()
    User.objects.exclude(is_superuser=True).delete()

    print("Creating users...")

    users = [
        create_user("tess@gla.ac.uk", "Tess", "Byrne", "100001", Decimal("80")),
        create_user("robert@gla.ac.uk", "Robert", "Scobie", "100002", Decimal("20")),
        create_user("ore@gla.ac.uk", "Ore", "Ajibade", "100003", Decimal("60")),
        create_user("radiance@gla.ac.uk", "Radiance", "Adegboyega", "100004", Decimal("45")),
        create_user("hayden@gla.ac.uk", "Hayden", "Gilmour", "100005", Decimal("70")),
        create_user("parisan@gla.ac.uk", "Parisan", "Vazirinejad", "100006", Decimal("30")),
        create_user("ben@gla.ac.uk", "Ben", "Ferenbach", "100007", Decimal("55")),
        create_user("maria@gla.ac.uk", "Maria", "Lopez", "100008", Decimal("90")),
    ]

    print("Creating items...")

    titles = [
        ("Desk Lamp", "Bright LED desk lamp", "ELECTRONICS", 12),
        ("Office Chair", "Comfortable ergonomic chair", "FURNITURE", 40),
        ("Uni Hoodie", "Warm hoodie size M", "CLOTHING", 18),
        ("Calculator", "Scientific calculator", "STATIONERY", 8),
        ("Football Boots", "Good condition boots", "SPORTS", 22),
        ("Textbook: Algorithms", "CS textbook barely used", "BOOKS", 25),
        ("Monitor 24 inch", "Full HD monitor", "ELECTRONICS", 65),
        ("Wooden Desk", "Study desk perfect for dorm", "FURNITURE", 55),
    ]

    items = []

    for title, desc, category, price in titles:
        seller = random.choice(users)

        item = Item.objects.create(
            seller=seller,
            title=title,
            description=desc,
            category=category,
            price=Decimal(price),
            status="AVAILABLE",
        )

        # add 1–3 photos
        for _ in range(random.randint(1, 3)):
            ItemPhoto.objects.create(
                item=item,
                url=random_image(),
                caption="Sample image",
            )

        items.append(item)

    print("Creating top-up transactions...")

    for user in users:
        amount = Decimal(random.randint(10, 50))
        Transaction.objects.create(
            buyer=user,
            type="TOPUP",
            amount=amount,
        )
        user.account_balance += amount
        user.save(update_fields=["account_balance"])

    print("Creating purchase transactions...")

    available_items = items.copy()
    random.shuffle(available_items)

    for item in available_items[:5]:  # sell some items
        buyers = [u for u in users if u != item.seller]
        buyer = random.choice(buyers)

        if buyer.account_balance >= item.price:

            Transaction.objects.create(
                buyer=buyer,
                type="PURCHASE",
                amount=item.price,
                item=item,
            )

            # transfer funds
            seller = item.seller
            buyer.account_balance -= item.price
            seller.account_balance += item.price

            buyer.save(update_fields=["account_balance"])
            seller.save(update_fields=["account_balance"])

            item.status = "SOLD"
            item.save(update_fields=["status"])

    print("✅ Population complete!")


if __name__ == "__main__":
    populate()