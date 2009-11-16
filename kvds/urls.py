from django.conf.urls.defaults import *

urlpatterns = patterns('kvds.app.views',
    (r'^start-session/$', 'start_session'),
    (r'^kvds/$', 'kvds'),
    (r'^session/$', 'session'),
    (r'^prefix/$', 'prefix'),
)
