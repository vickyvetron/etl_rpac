from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializer import CompanySerializer, CorporateSerializer
from .models import Company, Corporate
from account.permission import IsAdminUser


import logging

logger = logging.getLogger(__name__)


class CompanyView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        """
        This method responsible for handle get request
        """
        context = {}
        response_status = status.HTTP_200_OK
        companys = Company.objects.all()
        serializer = CompanySerializer(companys, many=True)
        context['message'] = 'All Comapany data'
        context['status'] = True
        context['data'] = serializer.data
        return Response(context, status=response_status)

    def post(self, request):
        """
        This method responsible for handle post request
        """
        context = {}
        response_status = status.HTTP_200_OK
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context['message'] = "Company Created"
            context['status'] = True
            context['data'] = serializer.data
        else:
            context['message'] = serializer.errors
            context['status'] = False
            context['data'] = []
        return Response(context, status=response_status)


class SingleCompanyView(APIView):

    def get_object(self, id):
        """
        This method used for get company object
        """
        try:
            obj = Company.objects.get(id=id)
            return obj
        except Company.DoesNotExist:
            return False

    def get(self, request, id):
        """
        This method responsible for handle get request
        """
        context = {}
        response_status = status.HTTP_200_OK
        com_obj = self.get_object(id)
        if com_obj:
            serializer = CompanySerializer(com_obj)
            context['message'] = "Succesfully retrive the company data"
            context['status'] = True
            context['data'] = serializer.data
        else:
            context['message'] = "Company Not Found"
            context['status'] = False
            context['data'] = []
            response_status = status.HTTP_404_NOT_FOUND
        return Response(context, status=response_status)

    def put(self, request, id):
        """
        This method responsible for handle post request
        """
        context = {}
        response_status = status.HTTP_200_OK
        com_obj = self.get_object(id)
        if com_obj:
            serializer = CompanySerializer(com_obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                context['message'] = "Company details updated"
                context['status'] = True
                context['data'] = serializer.data
            else:
                context['message'] = serializer.errors
                context['status'] = False
                context['data'] = []
                response_status = status.HTTP_400_BAD_REQUEST
        else:
            context['message'] = "Company Not Found"
            context['status'] = False
            context['data'] = []
            response_status = status.HTTP_404_NOT_FOUND
        return Response(context, status=response_status)

    def delete(self, request, id):
        """
        This method responsible for handle delete request
        """
        logger.info("POST request arrived for 'delete company api' ")
        context = {}
        response_status = status.HTTP_200_OK
        try:
            user = Company.objects.get(id=id)
            user.delete()
            logger.info("POST request for 'delete comapny api'- succesfully delete company")
            context['message'] = "Company succesfully delete"
            context['data'] = []
            context['status'] = True
        except Company.DoesNotExist:
            logger.error("POST request for 'delete company' - faild because of user does not exists")
            context['message'] = "User not found"
            context['data'] = []
            context['status'] = False
            response_status = status.HTTP_404_NOT_FOUND

        return Response(context, status=response_status)
    



class CorporateView(APIView):
    """
    This class used for corporate view
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        context = {}
        response_status = status.HTTP_200_OK
        companys = Corporate.objects.all()
        serializer = CorporateSerializer(companys, many=True)
        context['message'] = 'All Corporate data'
        context['status'] = True
        context['data'] = serializer.data
        return Response(context, status=response_status)

    def post(self, request):
        context = {}
        response_status = status.HTTP_200_OK
        serializer = CorporateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context['message'] = "Corporate Created"
            context['status'] = True
            context['data'] = serializer.data
        else:
            context['message'] = serializer.errors
            context['status'] = False
            context['data'] = []
        return Response(context, status=response_status)




class SingleCorporateView(APIView):

    def get_object(self, id):
        """
        This method used for get coporate objects
        """
        try:
            obj = Corporate.objects.get(id=id)
            return obj
        except Corporate.DoesNotExist:
            return False

    def get(self, request, id):
        """
        This method used for retrive single corporate details
        """
        context = {}
        response_status = status.HTTP_200_OK
        com_obj = self.get_object(id)
        if com_obj:
            serializer = CorporateSerializer(com_obj)
            context['message'] = "Succesfully retrive the corporate data"
            context['status'] = True
            context['data'] = serializer.data
        else:
            context['message'] = "Company Not Found"
            context['status'] = False
            context['data'] = []
            response_status = status.HTTP_404_NOT_FOUND
        return Response(context, status=response_status)

    def put(self, request, id):
        """
        This method used for update corporte details
        """
        context = {}
        response_status = status.HTTP_200_OK
        com_obj = self.get_object(id)
        if com_obj:
            serializer = CorporateSerializer(com_obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                context['message'] = "Corporate details updated"
                context['status'] = True
                context['data'] = serializer.data
            else:
                context['message'] = serializer.errors
                context['status'] = False
                context['data'] = []
                response_status = status.HTTP_400_BAD_REQUEST
        else:
            context['message'] = "Corporate Not Found"
            context['status'] = False
            context['data'] = []
            response_status = status.HTTP_404_NOT_FOUND
        return Response(context, status=response_status)

    def delete(self, request, id):
        """
        This method responsible for handle delete request
        """
        logger.info("POST request arrived for 'delete Corporate api' ")
        context = {}
        response_status = status.HTTP_200_OK
        try:
            user = Corporate.objects.get(id=id)
            user.delete()
            logger.info("POST request for 'delete comapny api'- succesfully delete corporate")
            context['message'] = "Corporate succesfully delete"
            context['data'] = []
            context['status'] = True
        except Corporate.DoesNotExist:
            logger.error("POST request for 'delete corporate' - faild because of user does not exists")
            context['message'] = "Corporate not found"
            context['data'] = []
            context['status'] = False
            response_status = status.HTTP_404_NOT_FOUND

        return Response(context, status=response_status)
    
