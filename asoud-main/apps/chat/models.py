from django.utils.translation import gettext_lazy as _

from apps.base.models import models, BaseModel
from apps.users.models import User

# Create your models here.


class ChatConversation(BaseModel):
    participants = models.ManyToManyField(
        User,
        verbose_name=_('Participants'),
    )

    class Meta:
        db_table = 'chat_conversation'
        verbose_name = _('Chat conversation')
        verbose_name_plural = _('Chat conversations')

    def __str__(self):
        # TODO: Fix the method
        return str(self.id)


class ChatMessage(BaseModel):
    conversation = models.ForeignKey(
        ChatConversation,
        on_delete=models.CASCADE,
        related_name='messages',
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Sender'),
    )
    text = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Text'),
    )
    file = models.FileField(
        upload_to='chat/',
        blank=True,
        null=True,
        verbose_name=_('File'),
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name=_('Is read'),
    )

    class Meta:
        db_table = 'chat_message'
        verbose_name = _('Chat message')
        verbose_name_plural = _('Chat messages')

    def __str__(self):
        # TODO: Fix the method
        return str(self.id)
