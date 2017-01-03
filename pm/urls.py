from django.conf.urls import url
from . import views



urlpatterns = [
    url(r'api_login$', views.api_login, name='api_login'),
    url(r'api_logout$', views.api_logout, name='api_logout'),
    url(r'api_regist$', views.api_regist, name='api_regist'),
    url(r'api_post$', views.api_post_paint, name='api_post'),
    url(r'api_comment$', views.api_comment, name='api_comment'),

    url(r'api_timeline$', views.api_timeLine, name='api_timeline'),
    url(r'api_getcomment$', views.api_getComment, name='api_getcomment'),
    url(r'api_mywork$', views.api_mywork, name='api_mywork'),
    url(r'api_like$', views.api_like, name='api_like'),
    url(r'api_dislike$', views.api_dislike, name='api_dislike'),
    url(r'api_hottimeline$', views.api_hottimeline, name='api_hottimeline'),
    url(r'api_likestimeline$', views.api_likestimeline, name='api_likestimeline'),
    url(r'api_followsTimeLine$', views.api_followsTimeLine, name='api_followsTimeLine'),
    url(r'api_follow', views.api_follow, name='api_follow'),
    url(r'api_unfollow', views.api_unfollow, name='api_unfollow'),
    url(r'api_myinfo', views.api_myinfo, name='api_myinfo'),
    url(r'api_change_avatar', views.api_change_avatar, name='api_change_avatar'),
    url(r'api_get_messages', views.api_get_messages, name='api_get_messages'),
]