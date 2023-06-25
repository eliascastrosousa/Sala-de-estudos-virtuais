from django.urls import path
from .views import (
    lobby,
    rooms,
    chat,
    all_messages,
    create_room,
    edit_room,
    delete_room,
    announcements_list,
    edit_announcement,
    create_announcement,
    delete_announcement,
    roadmap,
    all_roadmaps,
    create_roadmap,
    edit_roadmap,
    delete_roadmap,
    create_document,
    delete_document,
    create_category,
    delete_category,
)

urlpatterns = [
    # Sala
    path("lobby/", lobby, name="lobby"),
    path("rooms/", rooms, name="rooms"),
    path("chat/<str:room_id>/", chat, name="chat"),
    path("criar_sala/", create_room, name="criar_sala"),
    path("editar_sala/<str:room_id>/", edit_room, name="editar_sala"),
    path("deletar_sala/<str:room_id>/", delete_room, name="deletar_sala"),
    path("adicionar_categoria/", create_category, name="adicionar_categoria"),
    path("deletar_categoria/<str:category_id>/", delete_category, name="deletar_categoria"),
    # Aviso
    path("avisos/<str:room_id>/", announcements_list, name="avisos"),
    path("criar_aviso/<str:room_id>/", create_announcement, name="criar_aviso"),
    path("editar_aviso/<str:room_id>/<str:announcement_id>/", edit_announcement, name="editar_aviso"),
    path("deletar_aviso/<str:room_id>/<str:announcement_id>/", delete_announcement, name="deletar_aviso"),
    # Roadmap
    path("roadmap/<str:room_id>/<str:roadmap_id>/", roadmap, name="roadmap"),
    path("roadmaps/<str:room_id>/", all_roadmaps, name="roadmaps"),
    path("criar_roadmap/<str:room_id>/", create_roadmap, name="criar_roadmap"),
    path("editar_roadmap/<str:room_id>/<str:roadmap_id>/", edit_roadmap, name="editar_roadmap"),
    path("deletar_roadmap/<str:room_id>/<str:roadmap_id>/", delete_roadmap, name="deletar_roadmap"),
    # Documento
    path("criar_documento/<str:room_id>/<str:roadmap_id>/", create_document, name="criar_documento"),
    path("deletar_documento/<str:room_id>/<str:document_id>/", delete_document, name="deletar_documento"),
    # Mensagens
    path("mensagens/<str:room_id>/", all_messages, name="mensagens"),
]
