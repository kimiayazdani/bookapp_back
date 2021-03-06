from rest_framework.decorators import api_view, authentication_classes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from account_management.models import Account
from account_management.serializers import (
    RegistrationSerializer,
)
from account_management.utils import Util


@api_view(['POST', ])
@authentication_classes([])
def registration_view(request):
    data = {}
    email = request.data.get('email', '0').lower()

    if validate_email(email) is not None:
        data['message'] = 'این ایمیل قبلا استفاده شده است.'
        data['response'] = 'Error'
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    username = request.data.get('username', '0')
    if validate_username(username) is not None:
        data['message'] = 'نام‌کاربری پیش از شما توسط دیگران استفاده شده است.'
        data['response'] = 'Error'
        return Response(data=data, status=status.HTTP_403_FORBIDDEN)

    password = request.data.get('password', '0')
    val = validate_password(password)
    if val[0] is None:
        data['message'] = val[1]
        data['response'] = 'Error'
        return Response(data, status=status.HTTP_403_FORBIDDEN)
    phone_number = request.data.get('number', '0')
    val = validate_phone_number(phone_number)
    if val:
        data['message'] = val
        data['response'] = 'Error'
        return Response(data, status=status.HTTP_403_FORBIDDEN)

    data = {
        'password': password,
        'email': email,
        'phone_number': request.data.get('number', '0'),
        'username': username
    }
    serializer = RegistrationSerializer(data=data)

    if serializer.is_valid():
        account = serializer.save()
        ser = RegistrationSerializer(account)
        data = ser.data
        token = RefreshToken.for_user(user=account)
        data['userId'] = account.pk
        data['profilePicture'] = account.avatar.url
        data['email'] = account.email
        data['username'] = account.username
        data['refresh_token'] = str(token)
        data['access_token'] = str(token.access_token)
        absurl = 'http://' + get_current_site(request).domain + reverse('verify-email') + "?token=" + data[
            'access_token']
        email_body = 'Hi ' + account.username + ' Use Link below to verify your email: \n' + absurl
        email_data = {'body': email_body, 'subject': 'Verify your email', 'user_email': account.email}
        account.save()
        Util.send_email(data=email_data)

        return Response(data=data, status=status.HTTP_200_OK)
    else:
        data = serializer.errors

        return Response(data=data, status=status.HTTP_403_FORBIDDEN)


def validate_phone_number(phone_number):
    if len(phone_number) != 11:
        return 'شماره تماس اشتباه است.'
    return None


def validate_email(email):
    try:
        account = Account.objects.get(email=email)
    except Account.DoesNotExist:
        return None
    if account != None:
        return email


def validate_username(username):
    try:
        account = Account.objects.get(username=username)
    except Account.DoesNotExist:
        return None
    if account != None:
        return username


def validate_password(passwd):
    SpecialSym = ['$', '@', '#', '%']
    val = {0: "not None", 1: "not any error"}

    if len(passwd) < 6:
        val[0] = None
        val[1] = 'رمز عبور کوتاه است!'
        return val
    if len(passwd) > 40:
        val[0] = None
        val[1] = 'رمز عبور خیلی بزرگ است!'
        return val
    if not any(char.isdigit() for char in passwd):
        val[0] = None
        val[1] = 'رمزعبور باید حداقل یک عدد داشته باشد.'
        return val
    if not any(char.isupper() for char in passwd):
        val[0] = None
        val[1] = 'رمزعبور شما باید حداقل یک حرف بزرگ داشته باشد.'
        return val
    if not any(char.islower() for char in passwd):
        val[0] = None
        val[1] = 'رمزعبور شما باید حداقل یک حرف کوچک داشته باشد.'
        return val

    if any(char in SpecialSym for char in passwd):
        val[0] = None
        val[1] = 'رمز عبور نباید کاراکتر های {@,#,%,$ } را داشته باشد.'
        return val
    return val
