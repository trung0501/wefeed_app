import logging
import random
import uuid
from apps.users.models import User
from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from .models import User
from .serializers import UserRegisterSerializer
from .serializers import UserSerializer
from .serializers import LoginSerializer
from .serializers import GoogleOAuthSerializer
from .serializers import ChangePasswordSerializer
from .serializers import UploadAvatarSerializer
from .serializers import TwoStepVerifySerializer
from .serializers import SendOTPSerializer
from .serializers import VerifyOTPSerializer
from .serializers import ResetPasswordRequestSerializer

# Create your views here.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

User = get_user_model()


# Đăng ký người dùng 
class RegisterView(APIView): 
    def post(self, request):
        email = request.data.get('email', '').strip()  
        if User.objects.filter(email__iexact=email).exists():
            return Response({'message': 'Email đã được sử dụng'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['email'] = email  

        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Đăng ký thành công'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Đăng nhập

logger = logging.getLogger(__name__)

class LoginView(APIView):
    def post(self, request):
        logger.info(" [LOGIN] Request received at %s", request.path)

        # 1. Lấy dữ liệu đầu vào
        email = request.data.get("email")
        password = request.data.get("password")
        logger.debug(" Input email: %s", email)  

        # 2. Kiểm tra dữ liệu có đủ không
        if not email or not password:
            logger.warning(" Thiếu email hoặc mật khẩu ")
            return Response({"error": "Yêu cầu email và mật khẩu"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 3. Tìm user theo email
            try:
                user = User.objects.get(email=email)
                logger.info(" Tìm thấy nguwoif dùng: id=%s, email=%s", user.id, user.email)
            except User.DoesNotExist:
                logger.error(" Không tìm thấy email người dùng: %s", email)
                return Response({"error": "Không tìm thấy người dùng"}, status=status.HTTP_404_NOT_FOUND)
        # 4. Kiểm tra mật khẩu
            if not check_password(password, user.password):
                logger.error(" Mật khẩu sai id=%s", user.id)
                return Response({"error": "Thông tin không hợp lệ"}, status=status.HTTP_401_UNAUTHORIZED)

            # 5. Tạo JWT token
            refresh = RefreshToken.for_user(user)
            logger.info(" Người dùng đăng nhập thành công id=%s", user.id)

            return Response({
                "message": "Đăng nhập thành công",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user_id": user.id
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception(" Ngoại lệ trong quá trình đăng nhập ")
            return Response({"error": "Lỗi máy chủ nội bộ"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
class GoogleOAuthView(APIView):
    def post(self, request):
        # Xử lý đăng nhập qua Google OAuth2
        serializer = GoogleOAuthSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        access_token = serializer.validated_data['access_token']

        try:
            # Xác thực token với Google
            idinfo = id_token.verify_oauth2_token(access_token, google_requests.Request())

            email = idinfo.get('email')
            name = idinfo.get('name')

            # Tìm hoặc tạo user
            user, created = User.objects.get_or_create(email=email, defaults={
                'username': email.split('@')[0],
                'name': name,
            })

            # Trả về JWT 
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': 'Token không hợp lệ hoặc không thể xác thực'}, status=status.HTTP_401_UNAUTHORIZED)
        
   
# class SSOLoginView(APIView):
#     def post(self, request):
#         # Xử lý đăng nhập qua SAML SSO      
#         return Response({'message': 'SSO logic here'}, status=status.HTTP_200_OK)


# class UserDetailView(APIView):
#     def get(self, request, id):
#         user = User.objects.filter(id=id).first()
#         if not user:
#             return Response({'error': 'Không tìm thấy người dùng'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = UserRegisterSerializer(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    def get(self, request, id):
        # lấy user theo id, nếu không có thì trả về 404
        user = get_object_or_404(User, id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    def get(self, request, id):
        # lấy user theo id, nếu không có thì trả về 404
        user = get_object_or_404(User, id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserUpdateView(APIView):
    def put(self, request, id):
        user = get_object_or_404(User, id=id)

        serializer = UserRegisterSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Cập nhật thành công', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    def put(self, request, id):
        # Xử lý đổi mật khẩu
        user = get_object_or_404(User, id=id)

        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        if not user.check_password(old_password):
            return Response({'error': 'Mật khẩu cũ không đúng'}, status=status.HTTP_401_UNAUTHORIZED)

        user.set_password(new_password)
        user.save()
        return Response({'message': 'Đổi mật khẩu thành công'}, status=status.HTTP_200_OK)


class UploadAvatarView(APIView):
    def put(self, request, id):
        # Xử lý upload hoặc thay avatar
        user = get_object_or_404(User, id=id)
        
        serializer = UploadAvatarSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Cập nhật avatar thành công'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TwoStepSetupView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({'error': 'Không tìm thấy người dùng'}, status=status.HTTP_404_NOT_FOUND)
        
        # Bật xác thực 2 bước
        user.two_step_auth = True
        user.save()
        return Response({'message': 'Đã bật xác thực 2 bước'}, status=status.HTTP_200_OK)


class SendOTPView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'error': 'Không tìm thấy người dùng'}, status=status.HTTP_404_NOT_FOUND)

        # Sinh mã OTP ngẫu nhiên 6 số
        otp_code = str(random.randint(100000, 999999))

        # Lưu vào cache với thời gian hết hạn 5 phút
        cache.set(f"otp_user_{user.id}", otp_code, timeout=300)

        # Gửi email OTP
        send_mail(
            subject="Mã OTP xác thực",
            message=f"Mã OTP của bạn là: {otp_code}. Mã này sẽ hết hạn sau 5 phút.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response({'message': 'OTP đã được gửi qua email'}, status=status.HTTP_200_OK)


class TwoStepVerifyView(APIView):
    def post(self, request):
        # Xác minh mã OTP 
        serializer = TwoStepVerifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user_id = serializer.validated_data['user_id']
        otp_code = serializer.validated_data['otp_code']
    
        # Tìm user
        user = User.objects.get(id=user_id)
        # user = User.objects.filter(id=id).first()
        if not user:
            return Response({'error': 'Không tìm thấy người dùng'}, status=status.HTTP_404_NOT_FOUND)
        
        # Lấy OTP từ cache
        saved_otp = cache.get(f"otp_user_{user.id}")
        if saved_otp is None:
            return Response({'error': 'OTP đã hết hạn hoặc chưa được gửi'}, status=status.HTTP_400_BAD_REQUEST)

        if otp_code != saved_otp:
            return Response({'error': 'Mã OTP không hợp lệ'}, status=status.HTTP_400_BAD_REQUEST)

        # Xác minh thành công → xóa OTP khỏi cache
        cache.delete(f"otp_user_{user.id}")
        return Response({'message': 'Xác minh 2 bước thành công'}, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_id = serializer.validated_data['user_id']
        otp_code = serializer.validated_data['otp_code']

        # Tìm user
        user = User.objects.get(id=user_id)
        # user = User.objects.filter(id=id).first()
        if not user:
            return Response({'error': 'Không tìm thấy người dùng'}, status=status.HTTP_404_NOT_FOUND)

        # Lấy OTP từ cache
        saved_otp = cache.get(f"otp_user_{user.id}")
        if saved_otp is None:
            return Response({'error': 'OTP đã hết hạn hoặc chưa được gửi'}, status=status.HTTP_400_BAD_REQUEST)
        if otp_code != saved_otp:
            return Response({'error': 'Mã OTP không hợp lệ'}, status=status.HTTP_400_BAD_REQUEST)

        # Xác minh thành công → xóa OTP khỏi cache
        cache.delete(f"otp_user_{user.id}")
        return Response({'message': 'Xác minh OTP thành công'}, status=status.HTTP_200_OK)


class ResetPasswordRequestView(APIView):
    def post(self, request):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'error': 'Không tìm thấy người dùng'}, status=status.HTTP_404_NOT_FOUND)

        # Sinh token ngẫu nhiên
        reset_token = str(uuid.uuid4())

        # Lưu token vào cache với thời gian hết hạn 15 phút
        cache.set(f"reset_password_{user.id}", reset_token, timeout=900)

        # Gửi email chứa token
        reset_link = f"https://your-frontend.com/reset-password?token={reset_token}&id={user.id}"
        send_mail(
            subject="Yêu cầu đặt lại mật khẩu",
            message=f"Nhấn vào link sau để đặt lại mật khẩu: {reset_link}\nLink sẽ hết hạn sau 15 phút.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response({'message': 'Email đặt lại mật khẩu đã được gửi'}, status=status.HTTP_200_OK)