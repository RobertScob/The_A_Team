import uuid
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

#custom user with UUID primary key and fields from specification
class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #primary key
    username = None #using email instead
    first_name = models.CharField(max_length=128, blank=True)
    last_name = models.CharField(max_length=128, blank=True)

    email = models.EmailField(max_length=256, unique=True)
    student_id = models.CharField(max_length=32, unique=True)
    profile_photo_url = models.CharField(max_length=512, blank=True)

    #simulated currency balance
    account_balance = models.DecimalField(max_digits=12, decimal_places=2,default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0.00"))])

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "student_id"]

    def __str__(self):
        return f"{self.email}"