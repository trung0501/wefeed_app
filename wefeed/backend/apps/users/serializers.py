from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'auth_type', 'two_stept_auth']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # Xác thưc hai bước sẽ được lưu nếu đã khai báo trong fields
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class GoogleOAuthSerializer(serializers.Serializer):
    access_token = serializers.CharField()

# class SSOLoginSerializer(serializers.Serializer):
#     saml_response = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'avatar_url', 'auth_type', 'two_stept_auth']
        read_only_fields = ['id', 'auth_type', 'two_stept_auth']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Mật khẩu mới phải có ít nhất 8 ký tự.")
        return value


class UploadAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['avatar_url'] 


class TwoStepSetupSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class TwoStepVerifySerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    otp_code = serializers.CharField(required=True, max_length=6)

    def validate_otp_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Mã OTP phải là số.")
        if len(value) != 6:
            raise serializers.ValidationError("Mã OTP phải gồm 6 chữ số.")
        return value
    

class VerifyOTPSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)  
    otp_code = serializers.CharField(required=True, max_length=6)

    def validate_otp_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Mã OTP phải là số.")
        if len(value) != 6:
            raise serializers.ValidationError("Mã OTP phải gồm 6 chữ số.")
        return value
   
    
class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)