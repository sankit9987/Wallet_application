from rest_framework import serializers
from app.models import *
from django.contrib.auth.models import User
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password')
    
    def validate(self, attrs):
        username = attrs.get('username')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("User already exits")
        return super().validate(attrs)
    
    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"
    

    def create(self, validated_data):
        amount = validated_data.get('amount')
        balance_type = validated_data.get('status')
        user = self.context.get('user')
        
        if balance_type=='add':
            wallet = Wallet.objects.create(user=user,amount=amount,status="add")
            total = Total_amount.objects.filter(user=user)
            if total:
                total[0].total = int(total[0].total)+int(amount)
                total[0].save()
                return wallet
                
            Total_amount.objects.create(user=user,total=amount)
            return wallet
        else:
            total = Total_amount.objects.filter(user=user)
            
            if total:
                total[0].total = int(total[0].total)-int(amount)
                if total[0].total>=0:
                    print("YEs")
                    wallet = Wallet.objects.create(user=user,amount=amount,status="remove")
                    total[0].save()
                    return wallet
                raise serializers.ValidationError("Insufficient money")
            raise serializers.ValidationError("Insufficient money")