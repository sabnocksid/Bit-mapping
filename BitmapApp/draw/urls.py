from django.urls import path
from . import views

urlpatterns = [
    path('', views.draw_view, name='draw'),
    path('process-drawing/', views.process_drawing, name='process_drawing'),
]
