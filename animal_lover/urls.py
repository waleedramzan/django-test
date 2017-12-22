from django.conf.urls import url
from views import *
urlpatterns = [
    url(r'^add/(?P<animal>[0-9]+)/$', AnimalView.as_view(), name='animail_view'),
    url(r'^delete/(?P<animal>[0-9]+)/$', DeleteAnimalView.as_view(), name='delete_animail_view'),
    url(r'^update/(?P<animal>[0-9]+)/$', UpdateAnimalView.as_view(), name='update_animail_view'),
    url(r'^user/signup/$', UserSignupAPIView.as_view(), name='user_signup'),
    url(r'^user/login/$', UserLoginAPIView.as_view(), name='user_login'),

]