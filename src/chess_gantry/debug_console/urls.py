from django.urls import path

from . import views

urlpatterns = [
    path("", views.console_page, name="console"),
    path("api/status", views.api_status, name="status"),
    path("api/ports", views.api_ports, name="ports"),
    path("api/log", views.api_log, name="log"),
    path("api/connect", views.api_connect, name="connect"),
    path("api/disconnect", views.api_disconnect, name="disconnect"),
    path("api/gcode", views.api_gcode, name="gcode"),
    path("api/stop", views.api_stop, name="stop"),
]
