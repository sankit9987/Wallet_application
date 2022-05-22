from .serializer import *
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate,login
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

def get_token(user):
    refere = RefreshToken.for_user(user)
    return {'Access Token':str(refere.access_token)}


class UserRegisterView(APIView):

    def post(self,request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg':'User Created'})
        return Response(serializers.errors)

class LoginView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                tokrn = get_token(user)
                return Response({'token':tokrn})
            return Response({'error':'Invalid User'})
        return Response(serializer.errors)

class BalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,format=None):
        wallet = Wallet.objects.filter(user=request.user)
        serializers = WalletSerializer(wallet,many=True)
        return Response(serializers.data)

    def post(self,request):
        serializers = WalletSerializer(data=request.data,context={'user':request.user})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'data':serializers.data})
        return Response(serializerss.errors)
