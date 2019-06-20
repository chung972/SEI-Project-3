from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup', views.signup, name='signup'),
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),
    # path('user/<int:user_id>/update/', views.UserUpdate.as_view(), name='user_update'),
    path('user/<int:user_id>/update/', views.user_update, name='user_update'),
    path('user/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    # path('user/<int:pk>/', views.UserDetail.as_view(), name='my_account'),
    path('events/', views.EventList.as_view(), name='event_list'),
    path('events/create/', views.EventCreate.as_view(), name='events_create'),
    path('events/<int:pk>/', views.EventDetail.as_view(), name='events_detail'),
    path('events/<int:pk>/update/', views.EventUpdate.as_view(), name='events_update'),
    path('events/<int:pk>/delete/', views.EventDelete.as_view(), name='events_delete'),
    path('events/<int:event_id>/add_photo/', views.add_photo, name='add_photo'),
    path('events/<int:pk>/PhotoDelete/', views.PhotoDelete.as_view(), name='photo_delete'),
    path('events/<int:event_id>/assoc_user/<int:user_id>/', views.assoc_user, name='assoc_user'),
    path('events/<int:event_id>/unassoc_user/<int:user_id>/', views.unassoc_user, name='unassoc_user'),
    path('events/<int:event_id>/photo_gal/', views.photo_gal, name="photo_gallery"),
    

]