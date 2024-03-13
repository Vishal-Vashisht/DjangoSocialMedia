from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('signin/',views.signin, name='signin'),
    path('signup/',views.signup, name='signup'),
    path('logout/',views.logout, name='logout'),
    path('settings/',views.settings, name='settings'),
    path('postupload/',views.postupload, name='postupload'),
    path('likepost/',views.postlike, name='postlike'),
    path('profile/<str:pk>',views.userprofile, name='profile'),
    path('follow/',views.follow, name='follow'),

]