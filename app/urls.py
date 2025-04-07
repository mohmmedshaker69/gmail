from django.urls import path, include
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()

router.register('mail_group', views.EmailGroupViewSet, basename='mail_group')

router.register('send_email', views.EmailMessageViewSet, basename='send_email')

router.register('email_settings', views.EmailSettingsViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('email_groups_excel/', views.EmailGroupExcelAPIView.as_view(), name='email_group_excel'),
]
