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
        'GET': (IsAuthenticated),
        'POST': (IsAuthenticated),
    }
    serializer_class = GameSerializer
    def get(self, request):
        """Index request"""
        # Get all the games:
        games = Game.objects.all()
        # Filter the games by owner, so you can only see your owned games
        # games = Game.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = GameSerializer(games, many=True).data
        return Response({ 'games': data })

    def post(self, request):
        """Create request"""
        # Serialize/create game
        game = GameSerializer(data=request.data['game'])
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
        'GET': (IsAuthenticated),
        'PATCH': (IsAuthenticated),
        'DELETE': (IsAuthenticated),
    }
    def get(self, request, pk):
        """Show request"""
        # Locate the game to show
        game = get_object_or_404(Game, pk=pk)
        # Only want to show owned games?
        # if not request.user.id == game.owner.id:
        #     raise PermissionDenied('Unauthorized, you do not own this game')

        # Run the data through the serializer so it's formatted
        data = GameSerializer(game).data
        return Response({ 'game': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate game to delete
        game = get_object_or_404(Game, pk=pk)
        # Check the game's owner agains the user making this request
        # if not request.user.id == game.owner.id:
        #     raise PermissionDenied('Unauthorized, you do not own this game')
        # Only delete if the user owns the  game
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Remove owner from request object
        # This "gets" the owner key on the data['game'] dictionary
        # and returns False if it doesn't find it. So, if it's found we
        # remove it.
        # if request.data['game'].get('owner', False):
        #     del request.data['game']['owner']

        # Locate Game
        # get_object_or_404 returns a object representation of our Game
        game = get_object_or_404(Game, pk=pk)
        # Check if user is the same as the request.user.id
        # if not request.user.id == game.owner.id:
        #     raise PermissionDenied('Unauthorized, you do not own this game')

        # Add owner to data object now that we know this user owns the resource
        # request.data['game']['owner'] = request.user.id
        # Validate updates with serializer
        data = GameSerializer(game, data=request.data['game'])
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
