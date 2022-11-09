from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializer import CompanySerializer, CorporateSerializer, GlobalConfigurationsSerializer, JobDetailsSerializer
from .models import Company, Corporate, GlobalConfiguration, JobDetail
from account.permission import IsAdminUser


import logging

logger = logging.getLogger(__name__)


class CompanyView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        """
        This method responsible for handle get request
        """
        logger.info('GET request arrived for company')
        context = {}
        response_status = status.HTTP_200_OK
        companys = Company.objects.all()
        serializer = CompanySerializer(companys, many=True)
        context['message'] = 'All Comapany data'
        context['status'] = True
        context['data'] = serializer.data
        logger.info('GET request arrived for company - succesfully get the all company data')
        return Response(context, status=response_status)

    def post(self, request):
        """
        This method responsible for handle post request
        """
        logger.info("POST request arrived for company api")
        context = {}
        response_status = status.HTTP_200_OK
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context['message'] = "Company Created"
            context['status'] = True
            context['data'] = serializer.data
            logger.info("POST request for create company- succesfully created comapny record")
        else:
            logger.error("POST request for comapny failed beacuse of request data not valid")
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
            logger.info("Get company object on retrive comapny data")
            obj = Company.objects.get(id=id)
            return obj
        except Company.DoesNotExist:
            logger.error("NO conapmy found with this id")
            return False

    def get(self, request, id):
        """
        This method responsible for handle get request
        """
        logger.info("GET request arrived for retrive comapny details")
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
        This method used for get corporate objects
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
    

class GlobalConfigurationsView(APIView):

    def get(self, request):
        context = {}
        response_status = status.HTTP_200_OK
        config_data = GlobalConfiguration.objects.all()
        serializer = GlobalConfigurationsSerializer(config_data, many=True)
        context['message'] = 'All Configurations data'
        context['status'] = True
        context['data'] = serializer.data
        return Response(context, status=response_status)

    def post(self, request):
        context = {}
        response_status = status.HTTP_200_OK
        serializer = GlobalConfigurationsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context['message'] = "Succesfully save settings data"
            context['status'] = True
            context['data'] = serializer.data
        else:
            context['message'] = serializer.errors
            context['status'] = False
            context['data'] = []
        return Response(context, status=response_status)


class AllGlobalConfigurationByCompany(APIView):

    def get_settings_by_company_name(self, company_name):
        try:
            setting = GlobalConfiguration.objects.filter(corporate__company__name=company_name)
            return setting
        except GlobalConfiguration.DoesNotExist:
            return False

    def get(self, request, company_name):
        context = {}
        response_status = status.HTTP_200_OK
        try:
            setting = self.get_settings_by_company_name(company_name)
            if setting:
                serializer = GlobalConfigurationsSerializer(setting, many=True)
                context['message'] = 'All Configurations data'
                context['status'] = True
                context['data'] = serializer.data
            else:
                context['message'] = 'No data found with this corporate name'
                context['status'] = False
                context['data'] = []
                response_status = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            context['message'] = str(e)
            context['status'] = False
            context['data'] = []
            response_status = status.HTTP_400_BAD_REQUEST
        return Response(context, status=response_status)


class SingleGlobalConfiguration(APIView):

    def get_config_obj(self, id):
        try:
            setting = GlobalConfiguration.objects.get(id=id)
            return setting
        except GlobalConfiguration.DoesNotExist:
            return False

    def get(self, request, id):
        context = {}
        response_status = status.HTTP_200_OK
        try:
            setting = self.get_config_obj(id)
            if setting:
                serializer = GlobalConfigurationsSerializer(setting)
                context['message'] = 'All Configurations data'
                context['status'] = True
                context['data'] = serializer.data
            else:
                context['message'] = 'No data found with this id'
                context['status'] = False
                context['data'] = []
                response_status = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            context['message'] = str(e)
            context['status'] = False
            context['data'] = []
            response_status = status.HTTP_400_BAD_REQUEST
        return Response(context, status=response_status)


    def put(self, request, id):
        context = {}
        response_status = status.HTTP_200_OK
        setting = self.get_config_obj(id)
        if setting:
            serializer = GlobalConfigurationsSerializer(setting, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                context['message'] = "Setting details updated"
                context['status'] = True
                context['data'] = serializer.data
            else:
                context['message'] = serializer.errors
                context['status'] = False
                context['data'] = []
                response_status = status.HTTP_400_BAD_REQUEST
        else:
            context['message'] = "Setting Not Found"
            context['status'] = False
            context['data'] = []
            response_status = status.HTTP_404_NOT_FOUND
        return Response(context, status=response_status)

    def delete(self, request, id):
        """
        This method responsible for handle delete request
        """
        logger.info("POST request arrived for 'delete setting details api' ")
        context = {}
        response_status = status.HTTP_200_OK
        try:
            user = GlobalConfiguration.objects.get(id=id)
            user.delete()
            logger.info("POST request for 'delete comapny api'- succesfully delete setting")
            context['message'] = "Setting succesfully delete"
            context['data'] = []
            context['status'] = True
        except GlobalConfiguration.DoesNotExist:
            logger.error("POST request for 'delete setting' - faild because of user does not exists")
            context['message'] = "Setting not found"
            context['data'] = []
            context['status'] = False
            response_status = status.HTTP_404_NOT_FOUND

        return Response(context, status=response_status)


class JobDetailsView(APIView):

    def get(self, request):
        context = {}
        response_status = status.HTTP_200_OK
        job_details = JobDetail.objects.all()
        serializer = JobDetailsSerializer(job_details, many=True)
        context['message'] = 'All Jobs data'
        context['status'] = True
        context['data'] = serializer.data
        return Response(context, status=response_status)

    def post(self, request):
        context = {}
        response_status = status.HTTP_200_OK
        serializer = JobDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context['message'] = 'Job Succesfully created'
            context['status'] = True
            context['data'] = serializer.data
        else:
            context['message'] = serializer.errors
            context['status'] = False
            context['data'] = []
        return Response(context, status=response_status)


class SingleJobDeatilsView(APIView):

    def get_job_obj(self, id):
        try:
            setting = JobDetail.objects.get(id=id)
            return setting
        except JobDetail.DoesNotExist:
            return False

    def get(self, request, id):
        context = {}
        response_status = status.HTTP_200_OK
        try:
            job = self.get_job_obj(id)
            if job:
                serializer = JobDetailsSerializer(job)
                context['message'] = 'Job Data'
                context['status'] = True
                context['data'] = serializer.data
            else:
                context['message'] = 'No data found with this id'
                context['status'] = False
                context['data'] = []
                response_status = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            context['message'] = str(e)
            context['status'] = False
            context['data'] = []
            response_status = status.HTTP_400_BAD_REQUEST
        return Response(context, status=response_status)

    def put(self, request, id):
        context = {}
        response_status = status.HTTP_200_OK
        job = self.get_job_obj(id)
        if job:
            serializer = JobDetailsSerializer(job, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                context['message'] = "Job details updated"
                context['status'] = True
                context['data'] = serializer.data
            else:
                context['message'] = serializer.errors
                context['status'] = False
                context['data'] = []
                response_status = status.HTTP_400_BAD_REQUEST
        else:
            context['message'] = "JOb Details Not Found"
            context['status'] = False
            context['data'] = []
            response_status = status.HTTP_404_NOT_FOUND
        return Response(context, status=response_status)

    def delete(self, request, id):
        """
        This method responsible for handle delete request
        """
        logger.info("POST request arrived for 'delete job details api' ")
        context = {}
        response_status = status.HTTP_200_OK
        try:
            user = JobDetail.objects.get(id=id)
            user.delete()
            logger.info("POST request for 'delete job api'- succesfully delete job")
            context['message'] = "Setting succesfully delete"
            context['data'] = []
            context['status'] = True
        except JobDetail.DoesNotExist:
            logger.error("POST request for 'delete job' - faild because of job does not exists")
            context['message'] = "Job not found"
            context['data'] = []
            context['status'] = False
            response_status = status.HTTP_404_NOT_FOUND

        return Response(context, status=response_status)