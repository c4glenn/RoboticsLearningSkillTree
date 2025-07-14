from celery import shared_task
from .models import SkillNode, Lesson, LessonStatus, SkillNodeStatus
from django.db import models

@shared_task
def update_skill_node_status(user_id):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.get(pk=user_id)
    all_skill_nodes = SkillNode.objects.all().prefetch_related('lessons')
    
    node_status = {}
    for node in all_skill_nodes:
        lessons = node.lessons.all()
        if not lessons.exists():
            node_status.add(node, 100)
            continue
        
        completed_count = LessonStatus.objects.filter(user=user, lesson__in=lessons, completed=True).count()
        if completed_count == lessons.count():
            node_status.add(node, 100)
        else:
            progress = LessonStatus.objects.filter(user=user, lesson__in=lessons).aggregate(
                total_progress=models.Sum('progress'))['total_progress'] or 0
            progress_percentage = (progress / (lessons.count() * 100)) * 100
            node_status.add(node, progress_percentage)
        
    for node in all_skill_nodes:
        prequisites = node.prerequisites.all()
        unlocked = all(node_status[preq] == 100 for preq in prequisites)
        
        SkillNodeStatus.objects.update_or_create(
            user=user,
            skill_node=node,
            defaults={
                'unlocked': unlocked,
                'completed': True if node_status[node] == 100 else False,
                'progress': node_status[node]}
        )