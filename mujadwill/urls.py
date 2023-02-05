from mujadwill import views
from django.urls import path
urlpatterns = [
    path('upload-sections/', views.upload_sections.as_view(), name='upload_sections'),
]
