from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Comment, CommentHistory

@receiver(pre_save, sender=Comment)
def track_comment_edit(sender, instance, **kwargs):
    if not instance.pk:
        return  # New comment; no history yet
    try:
        original = Comment.objects.get(pk=instance.pk)
    except Comment.DoesNotExist:
        return
    if original.content != instance.content:
        # Create history before saving the new content
        CommentHistory.objects.create(
            comment=original,
            previous_content=original.content,
            modified_by=instance.user,  # assumes `user` on instance is the editor
        )
