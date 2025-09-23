function sudokuSolver() {
    return  {
        grid: Array(9).fill().map(() => Array(9).fill('')),
        loading: false,
        message: '',
        messageType: 'success',
        csrfToken: document.querySelector('[name=csrf-token]').getAttribute('content'),        

        validateInput(event, i, j) {
            const value = event.target.value;
            if (value && (value < 1 || value > 9 || isNaN(value))) {
                this.grid[i][j] = '';
                event.target.value = '';
            }
            this.clearMessage();
        },

        async solvePuzzle() {
            this.loading = true;
            this.clearMessage();

            try {
                const response = await fetch('solve/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.csrfToken,
                    },
                    body: JSON.stringify({ grid: this.grid })
                });

                const data = await response.json();

                if (data.success) {
                    this.grid = data.grid.map(row => row.map(cell => cell === 0 ? '' : cell.toString()));
                    this.showMessage('Puzzle solved successfully!', 'success');
                } else {
                    this.showMessage(data.error || 'Failed to solve puzzle', 'error');
                }
            } catch (error) {
                this.showMessage('Error connecting to server', 'error');
            }

            this.loading = false;
        },
        async clearGrid() {
            this.loading = true;
            this.clearMessage();

            try {
                const response = await fetch('clear/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.csrfToken,
                    }
                });

                const data = await response.json();

                if(data.success) {
                    this.grid = data.grid;
                    this.showMessage('Grid cleared!', 'success');
                } else {
                    throw new Error('Server error');
                }
            } catch (error) {
                console.error('Error clearing grid:', error);
                this.grid = Array(9).fill().map(() => Array(9).fill(''));
                this.showMessage('Grid cleared!', 'success');
            }

            this.loading = false;
        },

        showMessage(text, type){
            this.message = text;
            this.messageType = type;
            setTimeout(() => this.clearMessage(), 3000);
        },

        clearMessage(){
            this.message = '';
        }
    }
}
