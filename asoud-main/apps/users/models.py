from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password

from .managers import CustomUserManager
from apps.base.models import models, BaseModel

# Create your models here.


class User(AbstractUser):
    USER = "user"
    OWNER = "owner"
    MARKETER = "marketer"

    TYPE_CHOICES = (
        (USER, _("User")),
        (OWNER, _("Owner")),
        (MARKETER, _("Marketer")),
    )

    # Authentication
    username = None
    mobile_number = models.CharField(
        unique=True,
        max_length=15,
        verbose_name=_('Mobile number'),
    )
    pin = models.CharField(
        max_length=128,  # Increased for hashed PIN storage
        verbose_name=_('Pin'),
        help_text=_('Hashed PIN for security')
    )
    pin_expiry = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Pin expiry')
    )
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default=USER,
        verbose_name=_('Type'),
    )

    USERNAME_FIELD = "mobile_number"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        db_table = 'user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.mobile_number

    def is_owner(self):
        return self.markets.exists()
    
    def set_pin(self, raw_pin):
        """Hash and set PIN securely"""
        self.pin = make_password(str(raw_pin))
    
    def check_pin(self, raw_pin):
        """Check if provided PIN matches stored hashed PIN"""
        return check_password(str(raw_pin), self.pin)

class UserProfile(BaseModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Address'),
    )
    national_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name=_('National code'),
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Birth date'),
    )
    iban_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_('Iban number'),
    )
    picture = models.ImageField(
        upload_to='user/picture/',
        blank=True,
        null=True,
        verbose_name=_('Image'),
    )

    class Meta:
        db_table = 'user_profile'
        verbose_name = _('User profile')
        verbose_name_plural = _('User profiles')

    def __str__(self):
        return self.mobile_number


class UserDocument(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User document'),
    )
    file = models.FileField(
        upload_to='user/document/',
        blank=True,
        null=True,
        verbose_name=_('Market file'),
    )

    class Meta:
        db_table = 'user_document'
        verbose_name = _('User document')
        verbose_name_plural = _('User documents')

    def __str__(self):
        return self.user


class UserColleague(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    mobile_number = models.CharField(
        unique=True,
        max_length=15,
        verbose_name=_('Mobile number'),
    )

    class Meta:
        db_table = 'user_colleague'
        verbose_name = _('User colleague')
        verbose_name_plural = _('User colleagues')

    def __str__(self):
        return self.user


class BankInfo(BaseModel):
    name = models.CharField(max_length=16, unique=True)
    logo = models.ImageField(
        upload_to='bank/logo/',
        blank=True,
        null=True,
        verbose_name=_('logo'),
    )
    def __str__(self):
        return self.name
    

class UserBankInfo(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='banks',
        verbose_name=_('User'),
    )
    bank_info = models.ForeignKey(
        BankInfo,
        on_delete=models.CASCADE,
        related_name='bankinfoes',
        verbose_name=_('Bank info'),
    )
    card_number = models.CharField(
        unique=True,
        max_length=19,
        verbose_name=_('Card number'),
    )
    account_number = models.CharField(
        unique=True,
        max_length=32,
        verbose_name=_('Account number'),
    )
    iban = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        verbose_name=_('Iban number'),
    )
    full_name = models.CharField(
        max_length=128,
        verbose_name=_('Full name'),
    )
    branch_id = models.PositiveSmallIntegerField(
        verbose_name=_('Branch id'),
    )
    branch_name = models.CharField(
        max_length=20,
        verbose_name=_('Branch name'),
    )
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.card_number
