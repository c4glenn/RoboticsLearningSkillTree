from rest_framework import viewsets, permissions
from .models import SkillNode, Lesson, UserProgress
from .serializers import SkillNodeSerializer, LessonSerializer, UserProgressSerializer



class SkillNodeViewSet(viewsets.ModelViewSet):
    """ViewSet for SkillNode model."""
    queryset = SkillNode.objects.all().order_by('order').prefetch_related('prerequisites')
    serializer_class = SkillNodeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class LessonViewSet(viewsets.ModelViewSet):
    """ViewSet for Lesson model."""
    queryset = Lesson.objects.filter(approved=True).order_by('order').prefetch_related('author', 'skill_node')
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
class UserProgressViewSet(viewsets.ModelViewSet):
    """ViewSet for UserProgress model."""
    serializer_class = UserProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return UserProgress.objects.filter(user=user).select_related('lesson', 'lesson__skill_node')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)