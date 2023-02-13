from mujadwill import views
from django.urls import path

urlpatterns = [
    path('import-sections/', views.import_sections.as_view(), name='import_sections'),
    path('import-instructors/', views.import_instructors.as_view(), name='import_instructors'),

    path('generate-schedules/', views.generate_schedules.as_view(), name='generate_schedules'),
    path('get-schedules/', views.get_schedules.as_view(), name='get_schedules'),
    path('get_schedule/<int:id>/', views.get_schedule.as_view(), name='get_schedule'),
]
