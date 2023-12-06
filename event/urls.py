from django.urls import path

from event import views

urlpatterns = [
    path('event/', views.EventList.as_view()),
    path('event/<int:pk>/', views.EventListDetail.as_view()),
    path('event/types/', views.EventTypeList.as_view())
]