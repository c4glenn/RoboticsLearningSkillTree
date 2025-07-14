from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SkillNode(models.Model):
    """Model representing a skill node in the skill tree."""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='dependent_nodes')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def is_unlocked_for(self, user):
        """Check if the skill node is unlocked for the user."""
        if not self.prerequisites.exists():
            return True
        
        if self.user_progress.filter(user=user, unlocked=True).exists():
            return True
        
        return False
        
    
class SkillNodeStatus(models.Model):
    """Model representing the status of a skill node for a user."""
    user = models.ForeignKey(User, related_name='skill_node_status', on_delete=models.CASCADE)
    skill_node = models.ForeignKey(SkillNode, related_name='user_progress', on_delete=models.CASCADE)
    unlocked = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    progress = models.FloatField(default=0.0)  # Percentage of completion
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'skill_node')

    def __str__(self):
        return f"{self.user.username} - {self.skill_node.title}: {'Completed' if self.completed else 'Incomplete'}"

        
class Lesson(models.Model):
    """Model representing a lesson associated with a skill node."""
    skill_node = models.ForeignKey(SkillNode, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.JSONField(blank=True, null=True) 
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_community_contributed = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    author = models.ForeignKey(User, related_name='lessons', on_delete=models.SET_NULL, null=True, blank=True)
    

    def __str__(self):
        return f"{self.skill_node.title} - {self.title} ({'Community' if self.is_community_contributed else 'Official'})"

class LessonStatus(models.Model):
    """Model representing user progress in the skill tree."""
    user = models.ForeignKey(User, related_name='LessonStatus', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='user_progress', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    progress = models.FloatField(default=0.0)  # Percentage of completion
    last_accessed = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        status = "Completed" if self.completed else "Incomplete"
        return f"{self.user.username} - {self.lesson.title}: {status}"