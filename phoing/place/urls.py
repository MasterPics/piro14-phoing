from django.urls import path
from . import views

app_name = 'place'

urlpatterns = [
    #####################profile#######################
    path('', view=views.place_list, name='place_list'),
    path('map/', view=views.place_map, name='place_map'),
    path('create/', view=views.place_create, name='place_create'),
    path('detail/<int:pk>/',
         view=views.place_detail, name='place_detail'),
    path('<int:pk>/delete/',
         view=views.place_delete, name='place_delete'),
    path('<int:pk>/update/',
         view=views.place_update, name='place_update'),

    path('select/', view=views.place_select,
         name='place_select'),  # TODO : 나중에 삭제할 것


    # path('<int:pk>/comment_create/',
    #      view=views.place_comment_create, name='place_comment_create'),
    # path('<int:pk>/comment_delete/',
    #      view=views.place_comment_delete, name='place_comment_delete'),
    # path('save/', views.place_save, name='place_save'),

]
