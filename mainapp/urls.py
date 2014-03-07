from django.conf.urls import patterns, url

from mainapp import views

urlpatterns = patterns('',
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^post_new/', views.post_new, name='post_new'),
    url(r'^signup_do/', views.signup_do, name='signup_do'),
    url(r'^login_do/', views.login_do, name='login_do'),
    url(r'^cancel_post/', views.cancel_post, name='cancel_post'),
    url(r'^logout_do/', views.logout_do, name='logout_do'),
    url(r'^reserve/', views.reserve, name='reserve'),
    url(r'^accept/', views.accept, name='accept'),
)
