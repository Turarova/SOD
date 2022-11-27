from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from .serializers import *
from .tasks import send_confirmation_email


User = get_user_model()

class StudentRegisterView(APIView):
    def post(self, request):
        serializer = StudentRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_confirmation_email.delay(user.email, user.activation_code)
            return Response(serializer.data, status=status.HTTP_201_CREATED)



class DirectorRegisterView(APIView):
    def post(self, request):
        serializer = DirectorRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)



class LoginStudentView(TokenObtainPairView):
    serializer_class = LoginStudentSerializer


class LoginDirectorView(TokenObtainPairView):
    serializer_class = LoginDirectorSerializer


class ActivationView(APIView):
    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            code = serializer.validated_data['activation_code']
            user = get_object_or_404(User, activation_code = code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'msg': 'Student successfully activated'})




class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)


    def update(self, request, *args, **kwargs):
        object = request.user
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not object.check_password(request.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            object.set_password(request.data.get("new_password"))
            object.is_active = True
            object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    def post(self, request):
        serializer_class = PasswordResetEmailSerializer(data = request.data)
        # serializer = self.serializer_class(data=data)
        if serializer_class.is_valid(raise_exception=True):
            print("I'M OKEY")
            pass
        return Response('OK', 200)
