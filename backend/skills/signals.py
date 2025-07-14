from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SkillNode, Lesson, SkillNodeStatus, LessonStatus
from .tasks import update_skill_node_status

@receiver(post_save, sender=LessonStatus)
def schedule_status_recalc(sender, instance, **kwargs):
    """Signal to recalculate skill node status when a lesson status is saved."""
    # Schedule the task to update skill node status
    update_skill_node_status.delay(instance.user.id)