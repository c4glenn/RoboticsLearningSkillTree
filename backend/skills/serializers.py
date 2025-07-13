from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import SkillNode, Lesson, UserProgress

class SkillNodeSerializer(serializers.ModelSerializer):
    """Serializer for SkillNode model."""
    class Meta:
        model = SkillNode
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class LessonSerializer(serializers.ModelSerializer):
    """Serializer for Lesson model."""
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
        
class UserProgressSerializer(serializers.ModelSerializer):
    """Serializer for UserProgress model."""
    class Meta:
        model = UserProgress
        fields = '__all__'
        read_only_fields = ('last_accessed')

    def validate(self, data):
        """Ensure that progress is between 0 and 100."""
        if not (0 <= data.get('progress', 0) <= 100):
            raise serializers.ValidationError("Progress must be between 0 and 100.")
        return data

