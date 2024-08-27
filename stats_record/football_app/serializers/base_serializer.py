# serializers.py
from rest_framework import serializers

class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        read_only_fields = ['created_by', 'updated_by', 'created_at', 'updated_at']
