from rest_framework import serializers
from .models import Poll, Choice, Vote

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'

class ChoiceSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'

class PollSerializer(serializers.ModelSerializer):
    choice = ChoiceSerilizer(many=True, read_only=True, required=False)

    class Meta:
        model = Poll
        fields = '__all__'