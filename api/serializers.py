from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models.game import Game
from .models.user import User
from .models.review import Review
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('head', 'body', 'rating', 'game_id', 'owner')

class ReviewReadSerializer(ReviewSerializer):
    owner = serializers.StringRelatedField()
    game = serializers.StringRelatedField(source='game_id')
    class Meta:
        model = Review
        fields = ('id', 'head', 'body', 'rating', 'owner', 'game',)
        
class GameSerializer(serializers.ModelSerializer):
    reviews = ReviewReadSerializer(many=True, read_only=True)
    class Meta:
        model = Game
        fields = ('id', 'name', 'description', 'price', 'reviews',)

class UserSerializer(serializers.ModelSerializer):
    # This model serializer will be used for User creation
    # The login serializer also inherits from this serializer
    # in order to require certain data for login
    class Meta:
        # get_user_model will get the user model (this is required)
        # https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#referencing-the-user-model
        model = get_user_model()
        fields = ('id', 'email', 'password', 'username')
        extra_kwargs = { 'password': { 'write_only': True, 'min_length': 5 } }

    # This create method will be used for model creation
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

class UserRegisterSerializer(serializers.Serializer):
    # Require email, password, and password_confirmation for sign up
    email = serializers.CharField(max_length=100, required=True)
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(required=True)
    password_confirmation = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        # Ensure password & password_confirmation exist
        if not data['password'] or not data['password_confirmation']:
            raise serializers.ValidationError('Please include a password and password confirmation.')

        # Ensure password & password_confirmation match
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError('Please make sure your passwords match.')
        # if all is well, return the data
        return data

class ChangePasswordSerializer(serializers.Serializer):
    model = get_user_model()
    old = serializers.CharField(required=True)
    new = serializers.CharField(required=True)
