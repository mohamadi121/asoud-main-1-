from apps.base.admin import admin, BaseAdmin, BaseTabularInline

from .models import ChatConversation, ChatMessage

# Register your models here.


class ChatMessageTabularInline(BaseTabularInline):
    model = ChatMessage
    extra = 1

    fields = (
        'sender',
        'text',
        'file',
        'is_read',
    )


class ChatConversationAdmin(BaseAdmin):
    inlines = [
        ChatMessageTabularInline,
    ]

    fields = (
        'participants',
    ) + BaseAdmin.fields

    readonly_fields = BaseAdmin.readonly_fields


admin.site.register(ChatConversation, ChatConversationAdmin)
