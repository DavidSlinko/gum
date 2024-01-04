from django.urls import path
from .views import *

urlpatterns = [
    # path('', index, name='index'),
    # path('category/<int:pk>/', category_view, name='category'),
    # path('exercise/<int:pk>/', exercise_view, name='gumfuel_detail')
    #path('add_exercise/', add_exercise_view, name='add_exercise')


    path('', ExerciseListView.as_view(), name='index'),
    path('category/<int:pk>/', ExerciseListByCategory.as_view(), name='category'),
    path('exercise/<int:pk>/', ExerciseDetail.as_view(), name='gumfuel_detail'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register', register_user, name='register'),
    path('search/', SearchEx.as_view(), name='search'),
    path('save_comment/<int:pk>/', save_comments, name='save_comment'),
    path('add_exercise/', NewExercise.as_view(), name='add_exercise'),
    path('exercise/<int:pk>/update', ExerciseUpdate.as_view(), name='update'),
    path('exercise/<int:pk>/delete', ExerciseDelete.as_view(), name='delete'),
    path('profile/<int:pk>/', profile_view, name='profile'),
    path('edit_account/', edit_account_view, name='edit_account'),
    path('edit_profile/', edit_profile, name='edit_profile')
]