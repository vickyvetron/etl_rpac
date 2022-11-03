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
        """
        This method responsible for handle POST request
        """
        logger.info('POST request arrived for login')
        context = {}
        response_status = status.HTTP_200_OK
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.data['email'], password=serializer.data['password'])
            if not user:
                logger.info("POST request for 'login' failed as  email and password was not found. responding BAD request")
                context['message'] = "Invalid Credentials"
                context['status'] = False
                context['data'] = []
                response_status = status.HTTP_404_NOT_FOUND
            else:
                token, _ = Token.objects.get_or_create(user=user)
                context['message'] = "Succesfully login"
                context['status'] = True
                context['data'] = {
                    'token':token.key,
                    'user': UserSerializer(user).data
                }
                
                logger.info("POST request responded successfully for 'login'")
        else:
            logger.error("POST request for 'login' failed as  login cred was not found. responding BAD request")
            context['message'] = "Please provide username and password boath"
            context['status'] = False
            context['data'] = []
            response_status = status.HTTP_400_BAD_REQUEST
        return Response(context, status=response_status)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        This method responsible for handle POST request
        """
        logger.info("POST request arrived for logout")
        context = {}
        response_status = status.HTTP_200_OK
        try:
            token_obj = Token.objects.get(user=request.user)
            token_obj.delete()
            logger.info("POST request responded successfully for 'logout'")
            context['message'] = "Succesfully Logout"
            context['status'] = True
            context['data'] = []
        except Exception as e:
            logger.error(f"something error occoured- {str(e)}")
            context['message'] = "You are not login"
            context['status'] = False
            context['data'] = []
            response_status = status.HTTP_400_BAD_REQUEST
        return Response(context, status=response_status)


class ForgatePasswordView(APIView):
    """
    This class used for forgate user password
    """
    
    def post(self, request):
        """
        This method responsible for handle POST request
        """
        logger.info('POST request arrived for forgote password')
        context = {}
        response_status = status.HTTP_200_OK
        serializer = ForgatePasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.data['email'])
            except User.DoesNotExist:
                context['message'] = "User not found"
                context['status'] = False
                context['data'] = []
                response_status = status.HTTP_404_NOT_FOUND
                logger.error("POST request for 'forgate-password' failed as all user data not found with the given email. responding BAD request")
                return Response(context, status=response_status)
            otp = generate_otp()

            try:
                obj = Otp.objects.get(user=user, type='Forgate_Password')
                obj.otp = otp
                obj.save()
            except Otp.DoesNotExist:
                obj = Otp.objects.update_or_create(otp=otp, user=user, type='Forgate_Password')

            logger.info('POST request for forgote password - otp succesfully generated')
                
            mesg = f"Hi {user.email} your forgate password code is - {otp}"
            mail = mail_send("Forgate Password OTP", mesg, settings.EMAIL_HOST_USER, [serializer.data['email']])

            if mail:
                logger.info('POST request for forgote password - otp send on mail seccesfully')
                context['message'] = "OTP sent on your mail. please check your mail"
                context['status'] = True
                context['data'] = []
            else:
                logger.error("POST request for 'forgate-password' something wend wrong on mail send. responding BAD request")
                context['message'] = "something went wrong. please try again"
                context['status'] = False
                context['data'] = []
                response_status = status.HTTP_400_BAD_REQUEST
        else:
            logger.error("POST request for 'forgate-password' failed as all required data not found. responding BAD request")
            context['message'] = serializer.errors
            context['status'] = False
            context['data'] = []
            response_status = status.HTTP_400_BAD_REQUEST

        return Response(context, status=response_status)


class SavePasswordView(APIView):

    def post(self, request):
        """
        This method responsible for handle POST request
        """
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
                        context['message'] = "Succesfully change password"
                        context['status'] = True
                        context['data'] = []

            except Otp.DoesNotExist:
                context['message'] = "Invalid OTP"
                context['status'] = False
                context['data'] = []
                response_status = status.HTTP_400_BAD_REQUEST
        else:
            context['message'] = serializer.errors
            context['status'] = False
            context['data'] = []
            response_status = status.HTTP_400_BAD_REQUEST

        return Response(context, status=response_status)


class CreateSubAdminView(APIView):
    """
    This class used for create subadmin user and get all subamdin user
    """
    permission_classes = [IsAuthenticated]


    def get(self, request):
        """
        This method responsible for handle GET request
        """
        context = {}
        response_status = status.HTTP_200_OK
        user = User.objects.filter(role__name='subadmin')
        serializer = UserSerializer(user, many=True)
        context['message'] = 'All Sub admin user'
        context['status'] = True
        context['data'] = serializer.data
        return Response(context, status=response_status)

    def post(self, request):
        """
        This method responsible for handle POST request
        """
        context = {}
        response_status = status.HTTP_200_OK
        serializer = CreateUserSerializer(data=request.data)
        user_id = User.objects.filter(user_id=request.data.get('user_id')).filter()
        email = User.objects.filter(email=request.data.get('email')).first()
        if user_id:
            context['message'] = "User ID already Exists"
            context['status'] = False
            context['data'] = []
            response_status = status.HTTP_400_BAD_REQUEST
        elif email:
            context['message'] = "Email ID already Exists"
            context['status'] = False
            context['data'] = []
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

                context['message'] = "Succesfully create subAdmin"
                context['status'] = True
                context['data'] = serializer.data
                
            else:
                context['message'] = serializer.errors
                context['status'] = False
                context['data'] = []
                response_status = status.HTTP_400_BAD_REQUEST

        return Response(context, status=response_status)



class CreateAdminView(APIView):
    """
    This class used for create admin user and get all admin user
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        """
        This method responsible for handle GET request
        """
        context = {}
        response_status = status.HTTP_200_OK
        user = User.objects.filter(role__name='admin')
        serializer = UserSerializer(user, many=True)
        context['message'] = 'All admin user'
        context['status'] = True
        context['data'] = serializer.data
        return Response(context, status=response_status)

    def post(self, request):
        """
        This method responsible for handle POST request
        """
        context = {}
        response_status = status.HTTP_200_OK
        serializer = CreateUserSerializer(data=request.data)
        user_id = User.objects.filter(user_id=request.data.get('user_id')).filter()
        email = User.objects.filter(email=request.data.get('email')).first()
        if user_id:
            context['message'] = "User ID already Exists"
            context['status'] = False
            context['data'] = []
            response_status = status.HTTP_400_BAD_REQUEST
        elif email:
            context['message'] = "Email ID already Exists"
            context['status'] = False
            context['data'] = []
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

                context['message'] = "Succesfully create admin"
                context['status'] = True
                context['data'] = serializer.data

            else:
                context['message'] = serializer.errors
                context['status'] = False
                context['data'] = []
                
                response_status = status.HTTP_400_BAD_REQUEST

        return Response(context, status=response_status)


class CreateUserView(APIView):
    """
    This class used for craete user and get all user
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        """
        This method responsible for handle GET request
        """
        context = {}
        response_status = status.HTTP_200_OK
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        context['message'] = 'All user'
        context['status'] = True
        context['data'] = serializer.data
        return Response(context, status=response_status)

    def post(self, request):
        """
        This method responsible for handle POST request
        """
        context = {}
        response_status = status.HTTP_200_OK
        serializer = CreateUserSerializer(data=request.data)
        user_id = User.objects.filter(user_id=request.data.get('user_id')).filter()
        email = User.objects.filter(email=request.data.get('email')).first()
        if user_id:
            context['message'] = "User ID already Exists"
            context['data'] = []
            context['status'] = False
            response_status = status.HTTP_400_BAD_REQUEST
        elif email:
            context['message'] = "Email ID already Exists"
            context['data'] = []
            context['status'] = False
            response_status = status.HTTP_400_BAD_REQUEST
        else:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                context['message'] = "Succesfully create admin"
                context['data'] = serializer.data
                context['status'] = True
            else:
                context['message'] = serializer.errors
                context['data'] = []
                context['status'] = False
                response_status = status.HTTP_400_BAD_REQUEST

        return Response(context, status=response_status)


class EditDeleteUserView(APIView):
    """
    This view used for edit user and delete user. url takes user id 
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_user_by_email_user_id(self, email, user_id):
        """
        This medtho used for checking request email or user id already present or not
        """
        user = User.objects.filter(email=email).first()
        if User.objects.filter(email=email).first():
            return email, 'email'
        elif User.objects.filter(user_id=user_id).first():
            return user_id, 'user id'
        else:
            return None, None

    def put(self, request, id):
        """
        This method responsibel for handle put request
        """
        context = {}
        response_status = status.HTTP_200_OK
        user,type = self.get_user_by_email_user_id(request.data.get('email'), request.data.get('user_id'))
        if user:
            context['message'] = f"{type} already exists"
            context['data'] = []
            context['status'] = False
            response_status = status.HTTP_400_BAD_REQUEST
        else:
            try:
                user = User.objects.get(id=id)
                serializer = UserSerializer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    context['message'] = "User succesfully updtae"
                    context['data'] = serializer.data
                    context['status'] = True
                else:
                    context['message'] = serializer.errors
                    context['data'] = []
                    context['status'] = False
                    response_status = status.HTTP_400_BAD_REQUEST
            except User.DoesNotExist:
                context['message'] = "User not found"
                context['data'] = []
                context['status'] = False
                response_status = status.HTTP_404_NOT_FOUND

        return Response(context, status=response_status)

    def delete(self, request, id):
        """
        This method responsible for handle delete request
        """
        logger.info("POST request arrived for 'delete user api' ")
        context = {}
        response_status = status.HTTP_200_OK
        try:
            user = User.objects.get(id=id)
            user.delete()
            logger.info("POST request for 'delete user api'- succesfully delete user")
            context['message'] = "User succesfully delete"
            context['data'] = []
            context['status'] = True
        except User.DoesNotExist:
            logger.error("POST request for 'delete user' - faild because of user does not exists")
            context['message'] = "User not found"
            context['data'] = []
            context['status'] = False
            response_status = status.HTTP_404_NOT_FOUND

        return Response(context, status=response_status)