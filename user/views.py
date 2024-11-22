from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from utils.exceptions import handle_exceptions
from utils.permissions import IsOwnerOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken

# from ..utils import exceptions
from .serializer import UserSerializer
# Model
from django.contrib.auth import get_user_model, hashers
User = get_user_model()

# Create your views here.


class SignUpView(APIView):

    def post(self, request):
        new_user = UserSerializer(data=request.data)
        new_user.is_valid(raise_exception=True)
        new_user.save()
        return Response({
            'message': 'Signup successful',
            'user': new_user.data
        })


class SignInView(APIView):

    @handle_exceptions
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Find the user matching email
        user = User.objects.get(username=username)

        # Check the plain text password from the request body against the stored hash
        # Takes plain text as first argument, hash as second
        if hashers.check_password(password, user.password):
            # Generate token using simpleJWT
            print("entra en el if")
            token_pair = RefreshToken.for_user(user)

            serialized_user = UserSerializer(user)

            return Response({
                'user': serialized_user.data,
                'token': str(token_pair.access_token)
            })

        # Send 401 if passwords don't match
        return Response({'detail': 'Unauthorized'}, status.HTTP_401_UNAUTHORIZED)


class RetrieveDestroyUserView(APIView):
    # permission_classes = [IsOwnerOrReadOnly]

    @handle_exceptions
    def get(self, request, id):
        user = User.objects.get(pk=id)
        serialized_user = UserSerializer(user)
        return Response({
            'user': serialized_user.data,
        })

    @handle_exceptions
    def delete(self, request, id):
        # find user
        user = User.objects.get(pk=id)

        # check if user bein deleted and current user are the same
        if not (str(user.username) == str(request.user)):
            return Response({'detail': 'Unauthorized not the owner'}, status.HTTP_401_UNAUTHORIZED)

        # check permissions
        self.check_object_permissions(request, user)
        user.delete()
        # if deletion conrrect
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddFollow(APIView):
    @handle_exceptions
    def put(self, request, userId, storyId):
        user = User.objects.get(pk=userId)
        serialized_user = UserSerializer(user)

        followsList = serialized_user.data['follows'] + [storyId]
        serialized_user = UserSerializer(
            user, data={'follows': followsList}, partial=True)
        serialized_user.is_valid(raise_exception=True)
        serialized_user.save()

        return Response({'user': serialized_user.data}, status=status.HTTP_200_OK)


class RemoveFollow(APIView):

    def put(self, request, userId, storyId):
        user = User.objects.get(pk=userId)
        serialized_user = UserSerializer(user)
        # get follow list
        followsList = serialized_user.data['follows']

        # Remove the story id from the list
        try:
            followsList.remove(storyId)
        except ValueError:
            # if it cant be its not present
            return Response(status=status.HTTP_204_NO_CONTENT)

        serialized_user = UserSerializer(
            user, data={'follows': followsList}, partial=True)
        serialized_user.is_valid(raise_exception=True)
        serialized_user.save()

        return Response({'user': serialized_user.data}, status=status.HTTP_200_OK)
