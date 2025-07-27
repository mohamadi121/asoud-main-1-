from apps.base.models import BaseModel, models
from apps.product.models import Product
from apps.users.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
# Create your models here.

class Discount(BaseModel):
    TOP_LEFT = "top_left"
    TOP_RIGHT = "top_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_RIGHT = "bottom_right"

    POSITION_CHOICES = (
        (TOP_LEFT, _("Top Left")),
        (TOP_RIGHT, _("Top Right")),
        (BOTTOM_LEFT, _("Bottom Left")),
        (BOTTOM_RIGHT, _("Bottom Right")),
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={'model__in': ['product', 'market']}
    )

    object_id = models.UUIDField(
        verbose_name=_('Object ID')
    )

    content_object = GenericForeignKey(
        'content_type',
        'object_id',
    )

    owner = models.ForeignKey(
        User,
        related_name="user_discount",
        on_delete=models.CASCADE    
    )

    users = ArrayField(
        models.CharField(max_length=15), 
        verbose_name=_('Users'),
        blank=True, 
        default=list
    )

    code = models.CharField(
        max_length=16,
        verbose_name=_('Code'),
    )

    position = models.CharField(
        max_length=20,
        choices=POSITION_CHOICES,
        default=TOP_LEFT,
        verbose_name=_("Position"),
    )

    percentage = models.PositiveSmallIntegerField(
        verbose_name=_('Percentage'),
    )

    expiry = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Expiry'),
    )

    limitation = models.PositiveSmallIntegerField(
        verbose_name=_('Limitation'),
        help_text=_('Number of allowed uses'),
        default=1000
    )

    consumed = models.PositiveSmallIntegerField(
        verbose_name=_('Consumed'),
        help_text=_('Number of uses'),
        default=0
    )
    
    class Meta:
        db_table = 'discount'
        verbose_name = _('Discount')
        verbose_name_plural = _('Discounts')

    def __str__(self):
        return self.code
    
    def is_valid(self):
        """
        Check if the discount is still valid.
        """
        # Check if the discount is within the usage limit
        within_limit = self.limitation == 0 or self.consumed < self.limitation

        # Check if the discount is not expired
        not_expired = self.expiry is None or self.expiry >= timezone.now()

        return within_limit and not_expired

    is_valid.boolean = True  # Display as a boolean icon in the admin
    is_valid.short_description = _("Is Valid")
