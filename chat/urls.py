from django.urls import path
from .views import (
    landing,
    lobby,
    rooms,
    chat,
    create_room,
    announcements_list,
    edit_announcement,
    create_announcement,
    delete_announcement,
)

urlpatterns = [
    path("", landing, name="landing"),
    path("lobby/", lobby, name="lobby"),
    path("rooms/", rooms, name="rooms"),
    path("chat/<str:room_id>/", chat, name="chat"),
    path("criar_sala/", create_room, name="criar_sala"),
    path("avisos/<str:room_id>/", announcements_list, name="avisos"),
    path("criar_aviso/<str:room_id>/", create_announcement, name="criar_aviso"),
    path("editar_aviso/<str:room_id>/<str:announcement_id>/", edit_announcement, name="editar_aviso"),
    path("deletar_aviso/<str:room_id>/<str:announcement_id>/", delete_announcement, name="deletar_aviso"),
]
