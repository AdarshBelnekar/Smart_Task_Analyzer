from rest_framework import serializers
from datetime import datetime

class TaskInputSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)  # optional if client doesn't supply
    title = serializers.CharField(required=True)
    due_date = serializers.DateField(required=False, allow_null=True)
    estimated_hours = serializers.FloatField(required=False, default=1)
    importance = serializers.IntegerField(required=False, default=5)
    dependencies = serializers.ListField(
        child=serializers.CharField(), required=False, default=list
    )

    def validate_importance(self, value):
        if value is None:
            return 5
        if not (1 <= value <= 10):
            raise serializers.ValidationError("importance must be 1-10")
        return value

    def validate_estimated_hours(self, value):
        try:
            if value < 0:
                raise serializers.ValidationError("estimated_hours must be >= 0")
        except TypeError:
            raise serializers.ValidationError("estimated_hours must be a number")
        return value

class TaskOutputSerializer(TaskInputSerializer):
    score = serializers.FloatField()
    explanation = serializers.CharField()
