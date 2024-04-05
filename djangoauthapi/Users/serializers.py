from rest_framework import serializers
from .models import User
from django.utils.encoding import smart_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['email', 'name', 'password','password2','cnic','city']
        extra_kwrgs={'password':{'write_only':True}}

    def create(self, validated_data):
        pass1 = validated_data.get('password')
        pass2 = validated_data.pop('password2')
        if pass1 != pass2:
            raise serializers.ValidationError("your passwords doesnot match")
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = User
        fields= ['email','password']
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['email', 'name','cnic','city']
        
class ChangePassSerializer(serializers.Serializer):
    password1= serializers.CharField(style={'input_type':'password'},write_only=True)
    password2= serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        fields = ['password1','password2']
    def validate(self, attrs):
        pass1 = attrs.get('password1')
        pass2 = attrs.pop('password2')
        user= self.context.get('user')
        if pass1 != pass2:
            raise serializers.ValidationError("your passwords doesnot match")
        user.set_password(pass1)
        user.save()
        return attrs
class PassResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    class Meta:
        fields = ['email']
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            print(user)
            uid = urlsafe_base64_encode(force_bytes(user.id))
 
            token = PasswordResetTokenGenerator().make_token(user)

            LINK = 'http://localhost:3000/user/passwordreset/' + uid + '/' + token

            body = "click the following link to reset your password" + LINK
            data = {
                'subject' : 'password reset',
                'body' : body,
                'to_email': user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError("This User does not exists")

class PassResetSerializer(serializers.Serializer):
    password1= serializers.CharField(style={'input_type':'password'},write_only=True)
    password2= serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        fields = ['password1','password2']
    def validate(self, attrs):
        pass1 = attrs.get('password1')
        pass2 = attrs.pop('password2')
        if pass1 != pass2:
            raise serializers.ValidationError("your passwords doesnot match")    
        uid= self.context.get('uid')
        token= self.context.get('token')
        id = smart_str(urlsafe_base64_decode(uid))
        user = User.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user,token):
            raise serializers.ValidationError('Token is not valid or expired')  
        user.set_password(pass1)
        user.save()
        return attrs
