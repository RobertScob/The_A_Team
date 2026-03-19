import os
import django
import random
from decimal import Decimal
from django.core.files import File
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "marketplace.settings")
django.setup()

from market.models import User, Item, ItemPhoto, Transaction

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text.upper()}")
    print("="*60)

def print_status(action, item):
    print(f"  [+] {action.ljust(15)} | {item}")

def create_user(email, first, last, s_id, balance):
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            "first_name": first,
            "last_name": last,
            "student_id": s_id,
            "account_balance": Decimal(balance),
        },
    )
    if created:
        user.set_password("password123")
        user.save()
        print_status("USER CREATED", f"{first} {last} ({email})")
    return user

def populate():
    print_header("Initializing Campus Marketplace")
    

    ItemPhoto.objects.all().delete()
    Transaction.objects.all().delete()
    Item.objects.all().delete()
    User.objects.exclude(is_staff=True).delete()
    

    print_header("Creating Student Accounts")
    u_data = [
        ("robert@gla.ac.uk", "Robert", "Scobie", "200001", "150.00"),
        ("ore@gla.ac.uk", "Ore", "Ajibade", "200002", "50000.00"),
        ("tess@gla.ac.uk", "Tess", "Bryne", "200003", "120.50"),
        ("hayden@gla.ac.uk", "Hayden", "Gilmour", "200004", "300.00"),
        ("radiance@gla.ac.uk", "Radiance", "Adegboyega", "200005", "50.00"),
        ("parisan@gla.ac.uk", "Parisan", "Vazirinejad", "200006", "40.00"),
        ("murdo@gla.ac.uk", "Murdo", "MacLeod", "200007", "80.00"),
        ("callum@gla.ac.uk", "Callum", "Campbell", "200008", "95.00"),
        ("finlay@gla.ac.uk", "Finlay", "Graham", "200009", "10.00"),
        ("mhairi@gla.ac.uk", "Mhairi", "Smith", "200010", "500.00"),
        ("fiona@gla.ac.uk", "Fiona", "Aitken", "200011", "400.00"),
    ]
    
    users = [create_user(*data) for data in u_data]


    print_header("Stocking Marketplace")
    item_pool = [
        ("UofG Official Hoodie", "Size Medium, Navy Blue. Great for library sessions.", "CLOTHING", 25.00, "hoodie.jpg"),
        ("IKEA Desk - Hillhead", "Moving out of Hillhead, needs a new home.", "FURNITURE", 15.00, "desk.jpg"),
        ("Calculus for Engineers", "Core textbook for 1st year UofG engineering.", "BOOKS", 40.00, "textbook.jpg"),
        ("Glasgow Warriors Jersey", "Official jersey, worn once to Scotstoun.", "SPORTS", 35.00, "rugby.jpg"),
        ("Tunnock's Teacake Cushion", "A bit of Scottish kit for your room.", "FURNITURE", 12.00, "cushion.jpg"),
        ("Electric Kettle", "Perfect for late night study tea.", "ELECTRONICS", 8.00, "kettle.jpg"),
        ("Lab Coat - Science", "Clean, fits someone 5'10. Used in The Wolfson Centre.", "CLOTHING", 15.00, "coat.jpg"),
        ("Bicycle - West End", "Rusty but works. Great for cycling down Byres Rd or a quick trip to central.", "OTHER", 50.00, "bicycle.jpg"),
        ("Noise Cancelling Headphones", "Crucial for the mid-day study in the JMS", "ELECTRONICS", 90.00, "headphones.jpg"),
        ("Macbeth - Annotated", "Shakespeare text for English Lit students.", "BOOKS", 5.00, "book.jpg"),
        ("Yoga Mat", "Used for classes at the Stevenson Hive.", "SPORTS", 10.00, "yoga.jpg"),
        ("Mini Fridge", "Keep your Irn Bru cold in the dorms.", "ELECTRONICS", 45.00, "fridge.jpg"),
        ("Desk Lamp", "LED lamp with USB port.", "STATIONERY", 12.50, "lamp.jpg"),
        ("Graphing Calculator", "Casio, essential for Maths 1.", "STATIONERY", 20.00, "calculator.jpg"),
        ("Winter Parka", "You'll need this for the Glasgow horizontal rain.", "CLOTHING", 60.00, "parka.jpg"),
        ("Toaster", "Two-slot toaster, works perfectly.", "ELECTRONICS", 10.00, "toaster.jpg"),
        ("Introduction to Psychology", "Barely used textbook.", "BOOKS", 30.00, "textbook-psy.jpg"),
        ("Gaming Mouse", "Logitech, used for 6 months.", "ELECTRONICS", 25.00, "mouse.jpg"),
        ("Buckfast", "My mate passed out before he could finish the bottle, so just selling the rest off.", "OTHER", 5.00, "buckfast.jpg"),
        ("GUSA Fleece Jacket", "Decided to become a chud. Stopped doing any sports or going outside.", "CLOTHING", 20.00, "fleece.jpg"),
        ("Pint of Fun", "Brewed fresh from my kitchen at Murano.", "OTHER", 20.00, "pint-of-fun.jpg"),
        ("Firewater Ticket", "Not gonna make it to my 8am tommorow if I go.", "OTHER", 12.00, "firewater.jpg"),
        ("Bapestas - Shoes", "Lowkey just need the money. Might not make it till my next SAAS payment", "CLOTHING", 18.00, "shoes.jpg"),
        ("MacBook Pro", "\"Strategically Invested\" all my savings - declaring bankruptcy.", "ELECTRONICS", 100.00, "macbook.jpg"),
        ("Bars of Gold", "Just won the lottery, feeling quite generous today", "OTHER", 20.00, "gold.jpg"),
    ]

    for title, desc, cat, price, filename in item_pool:
        seller = random.choice(users)
        item = Item.objects.create(
            seller=seller,
            title=title,
            description=desc,
            category=cat,
            price=Decimal(price),
            status="AVAILABLE"
        )
        
        full_path = os.path.join(settings.MEDIA_DIR, "thumbnails", filename) 
        if os.path.exists(full_path):
            with open(full_path, 'rb') as f:
                item.thumbnail.save(filename, File(f), save=True)
            print_status("ITEM + IMAGE", title)
        else:
            print_status("ITEM (NO IMG)", f"{title} (File {filename} not found)")
        
        print_status("ITEM LISTED", f"{title} (£{price}) by {seller.first_name}")


    print_header("Simulating Recent Sales")
    all_items = list(Item.objects.all())
    random.shuffle(all_items)
    
    for item in all_items[:5]:
        buyer = random.choice([u for u in users if u != item.seller])
        if buyer.account_balance >= item.price:
            Transaction.objects.create(
                buyer=buyer,
                item=item,
                type="PURCHASE",
                amount=item.price
            )

            buyer.account_balance -= item.price
            item.seller.account_balance += item.price
            buyer.save()
            item.seller.save()

            item.status = "SOLD"
            item.save()
            print_status("SOLD", f"{item.title} bought by {buyer.first_name}")

    print_header("Population Complete ✅")
    print(f"Total Users: {User.objects.count()}")
    print(f"Total Items: {Item.objects.count()}")
    print("="*60)

if __name__ == "__main__":
    populate()