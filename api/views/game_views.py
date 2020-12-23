from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404

from ..models.game import Game
from ..serializers import GameSerializer, UserSerializer

# Create your views here.
class Games(generics.ListCreateAPIView):
    permission_classes_by_method = {
        'GET': (),
        'POST': (),
    }
    serializer_class = GameSerializer
    def get(self, request):
        """Index request"""
        # Get all the games:
        games = Game.objects.all()

        # Run the data through the serializer
        data = GameSerializer(games, many=True).data
        return Response({ 'games': data })

    def post(self, request):
        """Create request"""
        # Serialize/create game
        game = GameSerializer(data=request.data)
        # If the game data is valid according to our serializer...
        if game.is_valid():
            # Save the created game & send a response
            game.save()
            return Response({ 'game': game.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(game.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_permissions(self):
        print(self.request.method)
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_method[self.request.method]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes_by_method = {
        'GET': (),
        'PATCH': (),
        'DELETE': (),
    }
    serializer_class = GameSerializer
    def get(self, request, pk):
        """Show request"""
        # Locate the game to show
        game = get_object_or_404(Game, pk=pk)
        
        # Run the data through the serializer so it's formatted
        data = GameSerializer(game).data
        return Response({ 'game': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate game to delete
        game = get_object_or_404(Game, pk=pk)
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Locate game to update
        game = get_object_or_404(Game, pk=pk)

        data = GameSerializer(game, data=request.data)
        if data.is_valid():
            data.save()
            return Response({ 'game': data.data })
        # If the data is not valid, return a response with the errors
        return Response(game.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_permissions(self):
        print(self.request.method)
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_method[self.request.method]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
