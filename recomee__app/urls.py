from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_started, name= 'get_started'),
    path('career_results/', views.career_results, name='career_results'),
    # path('display_data/', views.display_data, name='display_data'),
    # path('no-results/', views.no_results, name='no_results')
]
