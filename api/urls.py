from django.urls import path
from api.views import Taskviewsetview,SignUpView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import ObtainAuthToken

router=DefaultRouter()

router.register("v2/task",Taskviewsetview,basename="task")

urlpatterns=[
    path("token",ObtainAuthToken.as_view()),
    path("register/",SignUpView.as_view())
]+router.urls