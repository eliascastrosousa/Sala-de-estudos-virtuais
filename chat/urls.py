from django.urls import path
from .views import *

urlpatterns = [
    path("", landing, name="landing"),
    path("lobby/", lobby, name="lobby"),
    path("rooms/", rooms, name="rooms"),
    path("chat/<str:room_id>/", chat, name="chat"),
    path("criar_sala/", criar_sala, name="criar_sala"),
    path("avisos/<str:room_id>/", announcements_list, name="avisos"),
]
