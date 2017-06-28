from django.conf.urls import url
from . import views

urlpatterns = [
    ## Index Routes
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^process_register$', views.process),
    url(r'^authenticate$', views.authenticate),
    url(r'^logout$', views.logout),

    ## XYZ Routes
    # url(r'^XYZ$', views.XYZ),
    # url(r'^XYZ/add$', views.add_XYZ),
    # url(r'^XYZ/create$', views.create_XYZ),
    # url(r'^XYZ/(?P<XYZ_id>\d+)/show', views.show_XYZ),
    # url(r'^XYZ/(?P<XYZ_id>\d+)/edit', views.edit_XYZ),
    # url(r'^XYZ/(?P<XYZ_id>\d+)/update', views.update_XYZ),
    # url(r'^XYZ/(?P<XYZ_id>\d+)/delete', views.destroy_XYZ),
]
