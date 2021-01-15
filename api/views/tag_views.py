from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404

from ..models.tag import Tag
from ..serializers import TagSerializer

# Create your views here.
class Tags(generics.ListCreateAPIView):
    permission_classes_by_method = {
        'GET': (),
        'POST': (),
    }
    serializer_class = TagSerializer
    def get(self, request):
        """Index request"""
        # Get all the tags:
        tags = Tag.objects.all()
        # Filter the tags by owner, so you can only see your owned tags
        # tags = Tag.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = TagSerializer(tags, many=True).data
        return Response({ 'tags': data })

    def post(self, request):
        """Create request"""
        # Serialize/create tag
        
        request.data['owner'] = request.user.id
        tag = TagSerializer(data=request.data)
        # If the tag data is valid according to our serializer...
        if tag.is_valid():
            # Save the created tag & send a response
            tag.save()
            return Response({ 'tag': tag.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(tag.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_permissions(self):
        print(self.request.method)
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_method[self.request.method]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes_by_method = {
        'GET': (),
        'PATCH': (),
        'DELETE': (),
    }
    serializer_class = TagSerializer
    def get(self, request, pk):
        """Show request"""
        # Locate the tag to show
        tag = get_object_or_404(Tag, pk=pk)
        # Only want to show owned tags?
        if not request.user.id == tag.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this tag')

        # Run the data through the serializer so it's formatted
        data = TagSerializer(tag).data
        return Response({ 'tag': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate tag to delete
        tag = get_object_or_404(Tag, pk=pk)
        # Check the tag's owner agains the user making this request
        if not request.user.id == tag.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this tag')
        # Only delete if the user owns the  tag
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""

        # Locate Tag
        # get_object_or_404 returns a object representation of our Tag
        tag = get_object_or_404(Tag, pk=pk)
        # Check if user is the same as the request.user.id
        if not request.user.id == tag.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this tag')

        # Add owner to data object now that we know this user owns the resource
        request.data['owner'] = request.user.id
        # Validate updates with serializer
        tag = TagSerializer(tag, data=request.data)
        if tag.is_valid():
            # Save & send a 204 no content
            tag.save()
            return Response({ 'tag': tag.data })
        # If the data is not valid, return a response with the errors
        return Response(tag.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_permissions(self):
        print(self.request.method)
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_method[self.request.method]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
