from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.views import TokenObtainPairView


from django.shortcuts import get_object_or_404

from .serializers import *
# from .helpers import send_confirmation_email, send_resetpassword_link
# Create your views here.


class StudentRegisterView(APIView):
    def post(self, request):
        print(2)
        serializer = StudentRegisterSerializer(data=request.data)
        print(3)
        if serializer.is_valid(raise_exception=True):
            print(4)
            user = serializer.save()
            print(5)
            # send_confirmation_email(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# class DirectorRegisterView(APIView):
#     def post(self, request):
#         serializer = DirectorRegisterSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             user = serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer



# class ActivationView(APIView):
#     def post(self, request):
#         serializer = ActivationSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             code = serializer.validated_data['activation_code']
#             user = get_object_or_404(Student, activation_code = code)
#             user.is_active = True
#             user.activation_code = ''
#             user.save()
#             return Response({'msg': 'Student successfully activated'})


class ActivationSerializer(Serializer):
    activation_code = CharField(required=True, write_only=True, max_length=255)
