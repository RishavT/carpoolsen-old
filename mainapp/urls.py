from django.conf.urls import patterns, url

from mainapp import views

urlpatterns = patterns('',
    url(r'^$', views.dashboard, name='dashboard')
)
