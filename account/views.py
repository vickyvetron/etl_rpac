import logging

logger = logging.getLogger(__name__)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


from .serializer import LoginSerializer, UserSerializer, ForgatePasswordSerializer, SavePasswordSerializer, CreateUserSerializer

from .utils import mail_send, generate_otp
from .models import Otp, Role

from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.hashers import make_password
from .permission import IsAdminUser

User = get_user_model()


class LoginView(APIView):
    """
    This view used for token based login
    """
    permission_classes = [AllowAny]

    def post(self, request):
        logger.info('POST request arrived for login')
        context = {}
        response_status = status.HTTP_200_OK
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.data['email'], password=serializer.data['password'])
            if not user:
                logger.info("POST request for 'login' failed as  email and password was not found. responding BAD request")
                context = {
                    'message':"Invalid Credentials",
                    "data":[],
                    "status":False
                }
                response_status = status.HTTP_404_NOT_FOUND
            else:
                token, _ = Token.objects.get_or_create(user=user)
                context = {
                    'message':"Succesfully Logina",
                    "data":{
                        'token':token.key,
                        'user': UserSerializer(user).data
                    },
                    "status":True
                }
                logger.info("POST request responded successfully for 'login'")
        else:
            logger.error("POST request for 'login' failed as  login cred was not found. responding BAD request")
            context = {
                'message':"Please provide username and password boath",
                "data":[],
                "status":False
            }
            response_status = status.HTTP_400_BAD_REQUEST
        return Response(context, status=response_status)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        logger.info("POST request arrived for logout")
        context = {}
        response_status = status.HTTP_200_OK
        try:
            token_obj = Token.objects.get(user=request.user)
            token_obj.delete()
            logger.info("POST request responded successfully for 'logout'")
            context = {
                'message': "Succesfully Logout",
                'data':[],
                'status':True
            }
        except Exception as e:
            logger.error(f"something error occoured- {str(e)}")
            context = {
                'message': "You are not login",
                'data':[],
                'status':False
            }
            response_status = status.HTTP_400_BAD_REQUEST
        return Response(context, status=response_status)


class ForgatePasswordView(APIView):
    
    def post(self, request):
        context = {}
        response_status = status.HTTP_200_OK
        serializer = ForgatePasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.data['email'])
            except User.DoesNotExist:
                context = {
                    'message': "User not found",
                    'data': [],
                    'status': False
                }
                response_status = status.HTTP_404_NOT_FOUND
            otp = generate_otp()

            try:
                obj = Otp.objects.get(user=user, type='Forgate_Password')
                obj.otp = otp
                obj.save()
            except Otp.DoesNotExist:
                obj = Otp.objects.update_or_create(otp=otp, user=user, type='Forgate_Password')
                
            mesg = f"Hi {user.email} your forgate password code is - {otp}"
            mail = mail_send("Forgate Password OTP", mesg, settings.EMAIL_HOST_USER, [serializer.data['email']])

            if mail:
                context = {
                    'message': "OTP sent on your mail. please check your mail",
                    'data': [],
                    'status': True
                }
            else:
                context = {
                    'message': "something went wrong. please try again",
                    'data': [],
                    'status': False
                }
                response_status = status.HTTP_400_BAD_REQUEST
        else:
            context = {
                'message': serializer.errors,
                'data': [],
                'status': False
            }
            response_status = status.HTTP_400_BAD_REQUEST

        return Response(context, status=response_status)


class SavePasswordView(APIView):

    def post(self, request):
        context = {}
        response_status = status.HTTP_200_OK
        serializer = SavePasswordSerializer(data=request.data)

        if serializer.is_valid():
            try:
                otp_obj = Otp.objects.get(user__email=serializer.data['email'], otp=serializer.data['otp'])
                if otp_obj:
                    if otp_obj.otp == serializer.data['otp']:
                        user = User.objects.filter(email=otp_obj.user.email).first()
                        user.password = make_password(serializer.data['password'])
                        user.save()
                        otp_obj.delete()
                        context = {
                            'message': "Succesfully change password",
                            'data': [],
                            'status': True
                        }

            except Otp.DoesNotExist:
                context = {
                    'message': "Invalid OTP",
                    'data': [],
                    'status': False
                }
            response_status = status.HTTP_400_BAD_REQUEST
        else:
            context = {
                'message': serializer.errors,
                'data': [],
                'status': False
            }
            response_status = status.HTTP_400_BAD_REQUEST

        return Response(context, status=response_status)


class CreateSubAdminView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        context = {}
        response_status = status.HTTP_200_OK
        user = User.objects.filter(role__name='subadmin')
        serializer = UserSerializer(user, many=True)
        context['message'] = 'All Sub admin user'
        context['status'] = True
        context['data'] = serializer.data
        return Response(context, status=response_status)

    def post(self, request):
        context = {}
        response_status = status.HTTP_200_OK
        serializer = CreateUserSerializer(data=request.data)
        user_id = User.objects.filter(user_id=request.data.get('user_id')).filter()
        email = User.objects.filter(email=request.data.get('email')).first()
        if user_id:
            context = {
                'message': "User ID already Exists",
                'data': [],
                'status': False
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif email:
            context = {
                'message': "Email ID already Exists",
                'data': [],
                'status': False
            }
            response_status = status.HTTP_400_BAD_REQUEST
        else:
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                try:
                    subadmin = Role.objects.get(name='subadmin')
                except Role.DoesNotExist:
                    subadmin = Role.objects.create(name='subadmin')
                
                user.role.add(subadmin)
                user.save()

                context = {
                    'message': "Succesfully create subAdmin",
                    'data': serializer.data,
                    'status': True
                }
            else:
                context = {
                    'message': serializer.errors,
                    'data': [],
                    'status': False
                }
                response_status = status.HTTP_400_BAD_REQUEST

        return Response(context, status=response_status)



class CreateAdminView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        context = {}
        response_status = status.HTTP_200_OK
        user = User.objects.filter(role__name='admin')
        serializer = UserSerializer(user, many=True)
        context['message'] = 'All admin user'
        context['status'] = True
        context['data'] = serializer.data
        return Response(context, status=response_status)

    def post(self, request):
        context = {}
        response_status = status.HTTP_200_OK
        serializer = CreateUserSerializer(data=request.data)
        user_id = User.objects.filter(user_id=request.data.get('user_id')).filter()
        email = User.objects.filter(email=request.data.get('email')).first()
        if user_id:
            context = {
                'message': "User ID already Exists",
                'data': [],
                'status': False
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif email:
            context = {
                'message': "Email ID already Exists",
                'data': [],
                'status': False
            }
            response_status = status.HTTP_400_BAD_REQUEST
        else:
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                try:
                    subadmin = Role.objects.get(name='admin')
                except Role.DoesNotExist:
                    subadmin = Role.objects.create(name='admin')
                
                user.role.add(subadmin)
                user.save()

                context = {
                    'message': "Succesfully create admin",
                    'data': serializer.data,
                    'status': True
                }
            else:
                context = {
                    'message': serializer.errors,
                    'data': [],
                    'status': False
                }
                response_status = status.HTTP_400_BAD_REQUEST

        return Response(context, status=response_status)


class CreateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        context = {}
        response_status = status.HTTP_200_OK
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        context['message'] = 'All user'
        context['status'] = True
        context['data'] = serializer.data
        return Response(context, status=response_status)

    def post(self, request):
        context = {}
        response_status = status.HTTP_200_OK
        serializer = CreateUserSerializer(data=request.data)
        user_id = User.objects.filter(user_id=request.data.get('user_id')).filter()
        email = User.objects.filter(email=request.data.get('email')).first()
        if user_id:
            context = {
                'message': "User ID already Exists",
                'data': [],
                'status': False
            }
            response_status = status.HTTP_400_BAD_REQUEST
        elif email:
            context = {
                'message': "Email ID already Exists",
                'data': [],
                'status': False
            }
            response_status = status.HTTP_400_BAD_REQUEST
        else:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                context = {
                    'message': "Succesfully create admin",
                    'data': serializer.data,
                    'status': True
                }
            else:
                context = {
                    'message': serializer.errors,
                    'data': [],
                    'status': False
                }
                response_status = status.HTTP_400_BAD_REQUEST

        return Response(context, status=response_status)


class EditUserView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        pass

    def delete(self, request, id):
        context = {}
        response_status = status.HTTP_200_OK
        try:
            user = User.objects.get(id=id)
            user.delete()
            context['message'] = "User succesfully delete"
            context['data'] = []
            context['status'] = True
        except User.DoesNotExist:
            context['message'] = "User not found"
            context['data'] = []
            context['status'] = False
            response_status = status.HTTP_404_NOT_FOUND
            
        return Response(context, status=response_status)