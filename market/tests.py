from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal 
from django.utils import timezone
from .models import (
    User,
    Item, 
    ItemPhoto, 
    Transaction,
)

class UserModelTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email = "tess@gla.ac.uk",
            password = "password123", 
            first_name = "Tess",
            last_name = "Byrne", 
            student_id = "3117688"
        )
        self.asssertEqual(user.email, "tess@gla.ac.uk")
        self.assertEqual(user.account_balance, Decimal("0.00"))
        self.assertTrue(user.check_password("password123"))

class ItemModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email = "roberttheseller@example.com",
            password = "rickandmorty",
            first_name = "Robert",
            last_name = "Scobie", 
            student_id = "12345"
        )

    def test_item_creation(self):
        item = Item.objects.create(
            seller=self.user,
            title="Wooden Chair",
            description="A strong oak chair",
            price=Decimal("10.00"),
            category="FURNITURE"
        )
        self.assertEqual(item.status, "AVAILABLE")

    def test_prohibited_keyword_validation(self):
        item = Item(
            seller=self.user,
            title="Food Hamper",
            description="Includes snacks",
            price=Decimal("5.00"),
            category="OTHER"
        )
        with self.assertRaises(ValidationError):
            item.full_clean()  # triggers validate_not_prohibited

class ItemPhotoTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="parisan@gla.ac.uk",
            password="pass987654321",
            first_name="Parisan",
            last_name="V",
            student_id="456789"
        )
        self.item = Item.objects.create(
            seller=self.user,
            title="Desk Lamp",
            description="IKEA lamp",
            price=Decimal("7.00"),
            category="ELECTRONICS"
        )

    
    def test_add_photo(self):
        photo = ItemPhoto.objects.create(
            item=self.item,
            url="http://example.com/photo1.jpg",
            caption="Front view"
        )
        self.assertEqual(photo.item, self.item)
        self.assertTrue(self.item.photos.exists())


class TransactionSignalTests(TestCase):
    def setUp(self):
        self.seller = User.objects.create_user(
            email="hayden@gla.ac.uk",
            password="012345",
            first_name="Hayden",
            last_name="Gilmour",
            student_id="123456",
            account_balance=Decimal("0.00")
        )
        self.buyer = User.objects.create_user(
            email="ore@gla.ac.uk",
            password="password",
            first_name="Ore",
            last_name="Adabaje",
            student_id="1234",
            account_balance=Decimal("20.00")
        )

        self.item = Item.objects.create(
            seller=self.seller,
            title="Calculator",
            description="Scientific calc",
            price=Decimal("10.00"),
            category="STATIONERY"
        )

    def test_topup_increases_balance(self):
        Transaction.objects.create(
            buyer=self.buyer,
            amount=Decimal("30.00"),
            type="TOPUP",
        )
        self.buyer.refresh_from_db()
        self.assertEqual(self.buyer.account_balance, Decimal("50.00"))

    def test_purchase_transaction_updates_balances(self):
        Transaction.objects.create(
            buyer=self.buyer,
            item=self.item,
            amount=Decimal("10.00"),
            type="PURCHASE",
        )

        self.buyer.refresh_from_db()
        self.seller.refresh_from_db()
        self.item.refresh_from_db()

        self.assertEqual(self.buyer.account_balance, Decimal("10.00"))
        self.assertEqual(self.seller.account_balance, Decimal("10.00"))
        self.assertEqual(self.item.status, "SOLD")

    def test_purchase_without_item_fails(self):
        tx = Transaction(
            buyer=self.buyer,
            amount=Decimal("10.00"),
            type="PURCHASE",
            item=None
        )
        with self.assertRaises(ValidationError):
            tx.full_clean()

    def test_topup_with_item_fails(self):
        tx = Transaction(
            buyer=self.buyer,
            type="TOPUP",
            amount=Decimal("10.00"),
            item=self.item
        )
        with self.assertRaises(ValidationError):
            tx.full_clean()

    def test_cannot_purchase_sold_item(self):
        # First purchase marks item SOLD
        Transaction.objects.create(
            buyer=self.buyer,
            item=self.item,
            amount=Decimal("10.00"),
            type="PURCHASE"
        )

        # Second buyer attempts to purchase
        buyer2 = User.objects.create_user(
            email="buyer2@example.com",
            password="pass1234",
            first_name="B2",
            last_name="User",
            student_id="SID300",
            account_balance=Decimal("20.00")
        )

        with self.assertRaises(ValidationError):
            Transaction.objects.create(
                buyer=buyer2,
                item=self.item,
                amount=Decimal("10.00"),
                type="PURCHASE",
            )

    def test_purchase_insufficient_balance(self):
        poor_buyer = User.objects.create_user(
            email="poor@example.com",
            password="pass1234",
            first_name="Poor",
            last_name="User",
            student_id="SID400",
            account_balance=Decimal("0.50")
        )

        with self.assertRaises(ValidationError):
            Transaction.objects.create(
                buyer=poor_buyer,
                item=self.item,
                amount=Decimal("10.00"),
                type="PURCHASE",
            )
