from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Organisation
from .serializers import UserSerializer, OrganisationSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        orgName = f"{user.first_name}'s Organisation"
        Organisation.objects.create(name=orgName, description=f"{user.first_name}'s default organisation")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'status': 'success',
            'message': 'Registration successful',
            'data': {
                'accessToken': str(refresh.access_token),
                'user': UserSerializer(user).data
            }
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'message': 'Login successful',
                'data': {
                    'accessToken': str(refresh.access_token),
                    'user': UserSerializer(user).data
                }
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'Bad request',
            'message': 'Authentication failed',
            'statusCode': 401
        }, status=status.HTTP_401_UNAUTHORIZED)


from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_detail(request, id):
    user = User.objects.filter(id=id).first()
    if user:
        return Response({
            'status': 'success',
            'message': 'User record retrieved',
            'data': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    return Response({
        'status': 'Bad request',
        'message': 'User not found',
        'statusCode': 404
    }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_organisations(request):
    user = request.user
    organisations = user.organisations.all()
    return Response({
        'status': 'success',
        'message': 'Organisations retrieved',
        'data': OrganisationSerializer(organisations, many=True).data
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_organisation(request):
    data = request.data
    serializer = OrganisationSerializer(data=data)
    if serializer.is_valid():
        organisation = serializer.save()
        organisation.users.add(request.user)
        return Response({
            'status': 'success',
            'message': 'Organisation created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response({
        'status': 'Bad Request',
        'message': 'Client error',
        'statusCode': 400
    }, status=status.HTTP_400_BAD_REQUEST)
