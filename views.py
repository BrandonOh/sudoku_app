from django.shortcuts import render
from django.http import JsonResponse
import json

# Create your views here.
def sudoku_solver(request):
    return render(request, 'sudoku_app/sudoku_solver.html')

# HTMX endpoint for solving sudoku puzzle
def solve_sudoku(request):
    if request.method == 'POST':
        try: 
            data = json.loads(request.body)
            grid = data.get('grid', [])

            for i in range(9):
                for j in range(9):
                    if grid[i][j] == '':
                        grid[i][j] = 0
                    else:
                        grid[i][j] = int(grid[i][j])
            if solve_puzzle(grid):
                return JsonResponse({'success': True, 'grid': grid})
            else:
                return JsonResponse({'success': False, 'error': 'No solution found'})    
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
        
    return JsonResponse({'success': False, 'error': 'Invalid request'})

# HTMX endpoint to clear the grid
def clear_sudoku(request):
    if request.method == 'POST':
        empty_grid = [['' for _ in range(9)] for _ in range(9)]
        return JsonResponse({'success': True, 'grid': empty_grid})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

# Backtracking algorithm to solve
def solve_puzzle(grid):
    def is_valid(grid, row, col, num):
        for x in range(9):
            if grid[row][x] == num:
                return False
            
        for x in range(9):
            if grid[x][col] == num:
                return False
            
        start_row = row - row % 3
        start_col = col - col % 3            
        for i in range(3):
            for j in range(3):
                if grid[i + start_row][j + start_col] == num:
                    return False
                
        return True
    
    def solve(grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    for num in range (1, 10):
                        if is_valid(grid, i, j, num):
                            grid[i][j] = num
                            if solve(grid):
                                return True
                            grid[i][j] = 0
                    return False
        return True
    
    return solve(grid)