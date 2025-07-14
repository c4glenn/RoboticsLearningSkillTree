from rest_framework.routers import DefaultRouter
from .views import SkillNodeViewSet, LessonViewSet, UserProgressViewSet, SkillTreeView
from django.urls import path, include

router = DefaultRouter()

router.register(r'skill-nodes', SkillNodeViewSet, basename='skillnode')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'user-progress', UserProgressViewSet, basename='userprogress')

urlpatterns = [
    path('', include(router.urls)),
    path('skill-tree/', SkillTreeView.as_view(), name='skill-tree-view'),
]
