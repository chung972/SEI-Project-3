from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup', views.signup, name='signup'),
    path('events/', views.EventList.as_view(), name='event_list'),
    path('events/create/', views.EventCreate.as_view(), name='events_create'),
    path('events/<int:pk>/', views.EventDetail.as_view(), name='events_detail'),
    path('events/<int:pk>/update/', views.EventUpdate.as_view(), name='events_update'),
    path('events/<int:pk>/delete/', views.EventDelete.as_view(), name='events_delete'),
    path('events/<int:event_id>/add_photo/', views.add_photo, name='add_photo'),
    # path('events/<int:event_id>/delete_photo/<int:photo_id>', views.delete_photo, name='delete_photo'),

]