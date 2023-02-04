from django.urls import path 
from . import views

app_name= "blog"
urlpatterns = [

    path("",views.blog,name="blog"),
    path('detail/<int:id>',views.detail,name='detail'),
    path('dastebandi/<int:id>',views.dastebandi,name='dastebandi'),
   
]
