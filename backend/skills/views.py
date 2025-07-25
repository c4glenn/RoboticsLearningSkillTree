from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import SkillNode, SkillNodeStatus, Lesson, LessonStatus
from .serializers import SkillNodeSerializer, SkillNodeStatusSerializer, LessonSerializer, LessonStatusSerializer



class SkillNodeViewSet(viewsets.ModelViewSet):
    """ViewSet for SkillNode model."""
    queryset = SkillNode.objects.all().order_by('order').prefetch_related('prerequisites')
    serializer_class = SkillNodeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class LessonViewSet(viewsets.ModelViewSet):
    """ViewSet for Lesson model."""
    queryset = Lesson.objects.filter(approved=True).order_by('order').prefetch_related('author', 'skill_node')
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Lesson.objects.filter(approved=True).order_by('order').prefetch_related('skill_node', 'author')
        return super().get_queryset()
    
class UserProgressViewSet(viewsets.ModelViewSet):
    """ViewSet for UserProgress model."""
    serializer_class = LessonStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return LessonStatus.objects.filter(user=user).select_related('lesson', 'lesson__skill_node')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
class SkillTreeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        statuses = SkillNodeStatus.objects.filter(user=request.user).select_related('skill_node')
        serializer = SkillNodeStatusSerializer(statuses, many=True, context={'request': request})
        return Response(serializer.data)
    
    
class SkillNodeDummyData(APIView):
    dummy_data = '''{
  "nodes": [
    {
      "id": "intro",
      "label": "Intro to Robotics",
      "position": { "x": 100, "y": 100 },
      "class": "bg-gray-800 text-white rounded-lg p-2 shadow-md"
    },
    {
      "id": "mobility",
      "label": "Mobility Systems",
      "position": { "x": 300, "y": 200 },
      "class": "bg-purple-800 text-white rounded-lg p-2 shadow-md"
    }
  ],
  "edges": [
    {
      "id": "e1-2",
      "source": "intro",
      "target": "mobility"
    }
  ]
}
'''
    def get(self, request):
        import json
        data = json.loads(self.dummy_data)
        return Response(data)