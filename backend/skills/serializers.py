from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import SkillNode, SkillNodeStatus, Lesson, LessonStatus

class SkillNodeSerializer(serializers.ModelSerializer):
    """Serializer for SkillNode model."""
    class Meta:
        model = SkillNode
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
        
    def get_unlocked(self, obj):
        """Check if the skill node is unlocked for the current user."""
        request = self.context.get('request')
        if not request:
            return False # if you can call this without going through the view somehow? 
        if not hasattr(request, 'user'):
            return False #i think django solves this with the annoynomous user, but just in case
        if request.user.is_anonymous:
            return False # Maybe anonymous users should have them all unlocked?
        
        return obj.is_unlocked_for(request.user)

class SkillNodeStatusSerializer(serializers.ModelSerializer):
    """Serializer for SkillNodeStatus model."""
    skill_node = SkillNodeSerializer(read_only=True)

    class Meta:
        model = SkillNodeStatus
        fields = '__all__'
        read_only_fields = ('user', 'skill_node', 'last_accessed')

    def validate(self, data):
        """Ensure that progress is between 0 and 100."""
        if not (0 <= data.get('progress', 0) <= 100):
            raise serializers.ValidationError("Progress must be between 0 and 100.")
        return data

class LessonSerializer(serializers.ModelSerializer):
    """Serializer for Lesson model."""
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
        
class LessonStatusSerializer(serializers.ModelSerializer):
    """Serializer for UserProgress model."""
    class Meta:
        model = LessonStatus
        fields = '__all__'
        read_only_fields = ('last_accessed')

    def validate(self, data):
        """Ensure that progress is between 0 and 100."""
        if not (0 <= data.get('progress', 0) <= 100):
            raise serializers.ValidationError("Progress must be between 0 and 100.")
        return data

