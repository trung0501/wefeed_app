from rest_framework import serializers
from .models import FeedbackSession

class FeedbackSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackSession
        fields = '__all__'