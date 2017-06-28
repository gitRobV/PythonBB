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

    ## Travels Routes
    url(r'^travels$', views.travels),
    url(r'^travels/add$', views.add_travels),
    url(r'^travels/create$', views.create_travels),
    url(r'^travels/destination/(?P<travel_id>\d+)$', views.show_travels),
    url(r'^travels/join/(?P<travel_id>\d+)$', views.join_travels),
    url(r'^travels/create_join$', views.create_join),


    # url(r'^travels/(?P<travels_id>\d+)/edit', views.edit_travels),
    # url(r'^travels/(?P<travels_id>\d+)/update', views.update_travels),
    # url(r'^travels/(?P<travels_id>\d+)/delete', views.destroy_travels),

    ## XYZ Routes
    # url(r'^XYZ$', views.XYZ),
    # url(r'^XYZ/add$', views.add_XYZ),
    # url(r'^XYZ/create$', views.create_XYZ),
    # url(r'^XYZ/(?P<XYZ_id>\d+)/show', views.show_XYZ),
    # url(r'^XYZ/(?P<XYZ_id>\d+)/edit', views.edit_XYZ),
    # url(r'^XYZ/(?P<XYZ_id>\d+)/update', views.update_XYZ),
    # url(r'^XYZ/(?P<XYZ_id>\d+)/delete', views.destroy_XYZ),
]
