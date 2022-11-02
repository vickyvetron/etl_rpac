from django.urls import path


from .views import LogoutView, LoginView, ForgatePasswordView, SavePasswordView, CreateSubAdminView, CreateAdminView, CreateUserView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('forgate-password', ForgatePasswordView.as_view()),
    path('logout', LogoutView.as_view(), name='auth_logout'),
    path('save-password', SavePasswordView.as_view()),
    path('subadmin-user', CreateSubAdminView.as_view()),
    path('admin-user', CreateAdminView.as_view()),
    path('user', CreateUserView.as_view())
]