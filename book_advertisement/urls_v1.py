from django.conf.urls import url, include
from rest_framework import routers

from book_advertisement.views import BookAdvertiseView
from book_advertisement.views import BookAdvertiseApproveView, GetAllPosts, GetAllUserPosts, GetPublicUserPosts

router = routers.DefaultRouter()
router.register('post', BookAdvertiseView, basename='post')

urlpatterns = [
    url(r'^approve/(?P<pk>\d+)/$', BookAdvertiseApproveView.as_view(), name='approve'),
    url(r'^all', GetAllPosts.as_view(), name='all'),
    url(r'^user-posts/$', GetAllUserPosts.as_view(), name='user-posts'),
    url(r'^(?P<username>[0-9a-zA-Z]+)/posts/$', GetPublicUserPosts.as_view(), name='public-posts-review')
] + router.urls
