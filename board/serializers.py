

from rest_framework import serializers
from .models import Board


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'

    def validate_title(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Title cannot be empty")
        return value

    def create(self, validated_data):

        try:

            board_instance = Board.objects.create(**validated_data)
            return board_instance
        except Exception as e:

            raise serializers.ValidationError(
                f"Error creating Board: {str(e)}")
