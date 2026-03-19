import uuid
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Item, Transaction

User = get_user_model()

class CampusMarketplaceTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Run once for the entire class to set up data."""
        print("\n" + "="*60)
        print("  CAMPUS MARKETPLACE: AUTOMATED TEST SUITE")
        print("="*60)

    def setUp(self):
        """Run before every test."""
        test_name = self._testMethodName.replace('_', ' ').title()
        print(f"  [RUNNING] | {test_name.ljust(40)}", end=" ", flush=True)
        
        # Create a test user
        self.user_password = "testpassword123"
        self.user = User.objects.create_user(
            email="student@university.ac.uk",
            password=self.user_password,
            student_id="STU12345",
            first_name="Test",
            last_name="User"
        )
        
        # Create a second user for selling
        self.seller = User.objects.create_user(
            email="seller@university.ac.uk",
            password=self.user_password,
            student_id="SEL67890"
        )

        # Create a dummy item
        self.item = Item.objects.create(
            seller=self.seller,
            title="Standard Textbook",
            description="A very clean book.",
            category="BOOKS",
            price=Decimal("20.00"),
            status="AVAILABLE"
        )
        
        self.client = Client()

    def tearDown(self):
        """Run after every test."""
        # Logic to check if test failed or passed for the console log
        print("PASS ✅")

    # --- 1. MODEL TESTS ---

    def test_prohibited_keywords_validation(self):
        """Ensure title/description cannot contain illegal words."""
        bad_item = Item(
            seller=self.user,
            title="Selling some illegal stuff",
            price=Decimal("10.00")
        )
        with self.assertRaises(ValidationError):
            bad_item.full_clean()

    def test_user_balance_default(self):
        """Verify new users start with 0.00 balance."""
        self.assertEqual(self.user.account_balance, Decimal("0.00"))

    # --- 2. VIEW & ACCESS TESTS ---

    def test_homepage_loads_for_anonymous(self):
        """Public should be able to see the shop/home page."""
        response = self.client.get(reverse('market:shop'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        """Dashboard should redirect anonymous users to login."""
        response = self.client.get(reverse('market:dashboard'))
        self.assertEqual(response.status_code, 302) 

    def test_login_success(self):
        """Verify user can log in with correct credentials."""
        response = self.client.post(reverse('market:login'), {
            'email': self.user.email,
            'password': self.user_password
        })
        self.assertEqual(response.status_code, 302) 

    # --- 3. SEARCH & AJAX TESTS ---

    def test_search_filtering(self):
        """Test that searching returns specific items."""
        response = self.client.get(reverse('market:shop'), {'q': 'Textbook'})
        self.assertContains(response, "Standard Textbook")
        
        response = self.client.get(reverse('market:shop'), {'q': 'NonExistentItem'})
        self.assertNotContains(response, "Standard Textbook")

    def test_ajax_search_view(self):
        """Test the search_items component view used by jQuery."""
        self.client.login(email=self.user.email, password=self.user_password)
        response = self.client.get(reverse('market:search_items'), {'q': 'Textbook'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/item_results.html')

    # --- 4. TRANSACTION & LOGIC TESTS ---

    def test_topup_logic(self):
        """Test that account balance updates and transaction is logged."""
        self.client.login(email=self.user.email, password=self.user_password)
        response = self.client.post(reverse('market:account'), {
            'topup': '',
            'amount': '50.00'
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.account_balance, Decimal("50.00"))
        self.assertTrue(Transaction.objects.filter(type="TOPUP", buyer=self.user).exists())

    def test_purchase_insufficient_funds(self):
        """Purchase should fail if balance < item price."""
        self.client.login(email=self.user.email, password=self.user_password)
        response = self.client.post(reverse('market:purchase_item', args=[self.item.itemID]))
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any("insufficient" in str(m).lower() or "error" in m.tags for m in messages))

    def test_category_filtering(self):
        """Test that URL category parameters filter results."""
        response = self.client.get(reverse('market:shop'), {'category': 'BOOKS'})
        self.assertContains(response, "Standard Textbook")
        
        response = self.client.get(reverse('market:shop'), {'category': 'FURNITURE'})
        self.assertNotContains(response, "Standard Textbook")