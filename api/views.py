from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


from .models import CustomUser, Invitation
from .serializers import (
    SignupSerializer, TokenSerializer, ProfileSerializer,
    MyProfileSerializer
)


class Signup(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SignupSerializer


class ObtainToken(generics.CreateAPIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.filter(
            phone=serializer.validated_data['phone'],
            confirm_code=serializer.validated_data['confirm_code'])
        if user.exists():
            user = CustomUser.objects.get(
                phone=serializer.validated_data['phone'])
            token = Token.objects.create(user=user)
            response = {
                'token': str(token.key),
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Profile(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    if request.method == 'POST':
        if Invitation.objects.filter(invitee=request.user).exists():
            return Response({'message': 'Вы уже активировали свой код!'})
        serializer = MyProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.filter(
            invite_code=serializer.validated_data['invite_code'])
        if user.exists():
            inviter = CustomUser.objects.get(
                invite_code=serializer.validated_data['invite_code'])
            Invitation.objects.create(inviter=inviter, invitee=request.user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Такого кода не существует!'})
    if request.method == 'GET':
        me = request.user
        serializer = ProfileSerializer(me)
        return Response(serializer.data)


