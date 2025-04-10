from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('instruction/', views.instruction, name='instruction'),
    path('instruction2/', views.instruction2, name='instruction2'),
    path('instruction3/', views.instruction3, name='instruction3'),
    path('policy/', views.policy, name='policy'),
    path('support/', views.support, name='technical-support'),
  # ✅ Corrected to only use once
    path('terms-service/', views.terms_service, name='terms-service'),
    path('copyright-claims/', views.copyright_claims, name='copyright-claims'),
    path('terms/', views.terms, name='terms'),
    path('copyright/', views.copyright_view, name='copyright'),



    # ✅ Enable the download functionality
    path('download/', views.download_video, name='download_video'),
]
