from django.conf.urls import patterns, url

from bestwatch import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='home'),
        url(r'^home/$', views.index),
        url(r'^home/(?P<loginFail>\d+)/', views.index),
        url(r'^explore/$', views.explore),
        url(r'^explore/(?P<genre_id>\d+)/', views.explore),
        url(r'^shows/detail/(?P<show_id>\d+)/', views.shows_detail),
        url(r'^checklogin/', views.checkLogin),
        url(r'^logout/', views.logout),
        url(r'^fblogin/', views.fblogin),
        url(r'^checkFBLogin/', views.checkFBLogin),
        url(r'^user/view_detail/(?P<user_id>\d+)/', views.user_view_detail),
        url(r'^user/edit/', views.user_edit, name='user_edit'),
        url(r'^add_rating/', views.add_rating),
        url(r'^add_review/', views.add_review),
)
