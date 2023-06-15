from django.urls import path
from .views import landing, lobby, rooms, chat, create_room, announcements_list, edit_announcement

urlpatterns = [
    path("", landing, name="landing"),
    path("lobby/", lobby, name="lobby"),
    path("rooms/", rooms, name="rooms"),
    path("chat/<str:room_id>/", chat, name="chat"),
    path("criar_sala/", create_room, name="criar_sala"),
    path("avisos/<str:room_id>/", announcements_list, name="avisos"),
    path("alterar_aviso/<str:room_id>/<str:announcement_id>/", edit_announcement, name="alterar_aviso"),
]
