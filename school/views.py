from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from django.shortcuts import get_object_or_404

from .serializers import *
# from .helpers import send_confirmation_email, send_resetpassword_link
# Create your views here.


class RegisterStudent(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            # send_confirmation_email(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)