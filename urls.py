from django.urls import path
from . import views

app_name = 'sudoku_app'

urlpatterns = [
    path('', views.sudoku_solver, name='sudoku_solver'),
    path('solve/', views.solve_sudoku, name='solve_sudoku'),
    path('clear/', views.clear_sudoku, name='clear_sudoku'),
]