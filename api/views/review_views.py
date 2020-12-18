from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404

from ..models.review import Review
from ..serializers import ReviewSerializer, ReviewReadSerializer, UserSerializer

# Create your views here.
class Reviews(generics.ListCreateAPIView):
    permission_classes_by_method = {
        'GET': (),
        'POST': (IsAuthenticated,),
    }
    serializer_class = ReviewSerializer
    def get(self, request):
        """Index request"""
        # Get all the reviews:
        reviews = Review.objects.all()
        # Filter the reviews by owner, so you can only see your owned reviews
        # reviews = Review.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = ReviewReadSerializer(reviews, many=True).data
        return Response({ 'reviews': data })

    def post(self, request):
        """Create request"""
        # Serialize/create review
        
        request.data['owner'] = request.user.id
        review = ReviewSerializer(data=request.data)
        # If the review data is valid according to our serializer...
        if review.is_valid():
            # Save the created review & send a response
            review.save()
            return Response({ 'review': review.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(review.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_permissions(self):
        print(self.request.method)
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_method[self.request.method]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes_by_method = {
        'GET': (),
        'PATCH': (IsAuthenticated,),
        'DELETE': (IsAuthenticated,),
    }
    serializer_class = ReviewSerializer
    def get(self, request, pk):
        """Show request"""
        # Locate the review to show
        review = get_object_or_404(Review, pk=pk)
        # Only want to show owned reviews?
        if not request.user.id == review.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this review')

        # Run the data through the serializer so it's formatted
        data = ReviewReadSerializer(review).data
        return Response({ 'review': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate review to delete
        review = get_object_or_404(Review, pk=pk)
        # Check the review's owner agains the user making this request
        if not request.user.id == review.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this review')
        # Only delete if the user owns the  review
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""

        # Locate Review
        # get_object_or_404 returns a object representation of our Review
        review = get_object_or_404(Review, pk=pk)
        # Check if user is the same as the request.user.id
        if not request.user.id == review.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this review')

        # Add owner to data object now that we know this user owns the resource
        request.data['owner'] = request.user.id
        # Validate updates with serializer
        review = ReviewSerializer(review, data=request.data)
        if review.is_valid():
            # Save & send a 204 no content
            review.save()
            return Response({ 'review': review })
        # If the data is not valid, return a response with the errors
        return Response(review.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_permissions(self):
        print(self.request.method)
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_method[self.request.method]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
