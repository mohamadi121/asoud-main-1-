from django.utils.translation import gettext_lazy as _

from apps.base.models import models, BaseModel
from apps.users.models import User
from apps.product.models import Product
from apps.affiliate.models import AffiliateProduct

# Create your models here.

    # def total_price(self):
    #     # TODO: Handle discount section
    #     return sum(item.total_price() for item in self.cartitem_set.all())

    # def total_items(self):
    #     return sum(item.quantity for item in self.cartitem_set.all())


class Order(BaseModel):
    CASH = "cash"
    ONLINE = "online"

    TYPE_CHOICES = (
        (CASH, _("Cash")),
        (ONLINE, _("Online")),
    )

    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"
    COMPLETED = "completed"
    FAILED = "failed"

    STATUS_CHOICES = (
        (PENDING, _("Pending")),
        (COMPLETED, _("Completed")),
        (FAILED, _("Failed")),
    )

    user = models.ForeignKey(
        User,
        related_name="orders",
        on_delete=models.CASCADE,
        verbose_name=_('User')
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Description')
    )
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        verbose_name=_('Type'),
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING,
        verbose_name=_('Status'),
    )
    owner_description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Owner Descriptions')
    )
    is_paid = models.BooleanField(
        default=False,
        verbose_name=_('Is Paid')
    )
    
    class Meta:
        ordering = ['-created_at']
        db_table = 'order'
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f"Order {str(self.id)[:6]}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())
    
    def total_items(self):
        return sum(item.quantity for item in self.items.all())
    
    @classmethod
    def get_or_create_order(cls, user):
        """Get or create a order (pending order) for the user"""
        order, created = cls.objects.get_or_create(
            user=user,
            status=cls.PENDING,
            defaults={
                'type': cls.ONLINE,  # default to online, can be changed at checkout
                'description': 'Shopping order'
            }
        )
        return order

class OrderItem(BaseModel):
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE,
        verbose_name=_('Order'),
    )
    product = models.ForeignKey(
        Product,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('Product'),
    )
    affiliate = models.ForeignKey(
        AffiliateProduct,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('Affiliate Product')
    )
    quantity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name=_('Quantity'),
    )

    class Meta:
        ordering = ['-created_at']
        db_table = 'order_item'
        verbose_name = _('Order item')
        verbose_name_plural = _('Order items')

    def __str__(self):
        if self.product:
            name = self.product.name
        elif self.affiliate:
            name = self.affiliate.name
        else:
            name = "unknown"
        return f"{self.quantity} x {name}"

    def total_price(self):
        if self.product:
            price = self.product.main_price
        elif self.affiliate:
            price = self.affiliate.price
        else: 
            price = 0
        return price * self.quantity


