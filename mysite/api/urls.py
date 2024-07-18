from django.urls import path
from . import views
from django.http import HttpResponse

urlpatterns = [
    path('recipes/', views.recipeView.as_view(), name='get_post_recipe'),
    path('recipes/<id>', views.recipeViewById.as_view(), name='get_put_delete_recipe_by_id'), 
    path('healthCheck/', lambda request: HttpResponse(status=200), name='healthCheck')
]

