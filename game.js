class NimGame {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.confirmButton = document.getElementById('confirmMove');
        this.restartButton = document.getElementById('restartGame');
        this.messageElement = document.getElementById('message');

        // settings
        this.WIDTH = 400;
        this.HEIGHT = 300;
        this.BACKGROUND_COLOR = '#008000';
        this.MATCH_COLOR = '#ffff00';
        this.SELECTED_COLOR = '#ff0000';
        this.MATCH_RADIUS = 10;
        this.ROW_SPACING = 50;
        this.MATCH_SPACING = 30;

        // state of the game
        this.piles = [1, 2, 3];
        this.selected = [];
        this.playerTurn = true;

        // event listeners
        this.canvas.addEventListener('click', this.handleClick.bind(this));
        this.confirmButton.addEventListener('click', this.playerMove.bind(this));
        this.restartButton.addEventListener('click', this.restartGame.bind(this));
        document.addEventListener('keydown', (e) => {
            if (e.key.toLowerCase() === 'r') {
                this.restartGame();
            }
        });

        this.drawMatches();
    }

    drawMatches() {
        this.ctx.fillStyle = this.BACKGROUND_COLOR;
        this.ctx.fillRect(0, 0, this.WIDTH, this.HEIGHT);

        const yOffset = 50;
        for (let row = 0; row < this.piles.length; row++) {
            const count = this.piles[row];
            for (let i = 0; i < count; i++) {
                const x = this.WIDTH / 2 - (count * this.MATCH_SPACING / 2) + i * this.MATCH_SPACING;
                const y = yOffset + row * this.ROW_SPACING;
                
                this.ctx.beginPath();
                this.ctx.arc(x, y, this.MATCH_RADIUS, 0, Math.PI * 2);
                this.ctx.fillStyle = this.selected.some(s => s[0] === row && s[1] === i) 
                    ? this.SELECTED_COLOR 
                    : this.MATCH_COLOR;
                this.ctx.fill();
                this.ctx.closePath();
            }
        }
    }

    handleClick(event) {
        if (!this.playerTurn) return;

        const rect = this.canvas.getBoundingClientRect();
        const mouseX = event.clientX - rect.left;
        const mouseY = event.clientY - rect.top;

        const yOffset = 50;
        for (let row = 0; row < this.piles.length; row++) {
            const count = this.piles[row];
            for (let i = 0; i < count; i++) {
                const x = this.WIDTH / 2 - (count * this.MATCH_SPACING / 2) + i * this.MATCH_SPACING;
                const y = yOffset + row * this.ROW_SPACING;
                
                const dist = Math.sqrt((mouseX - x) ** 2 + (mouseY - y) ** 2);
                if (dist <= this.MATCH_RADIUS) {
                    this.toggleMatch(row, i);
                    return;
                }
            }
        }
    }

    toggleMatch(row, index) {
        const matchIndex = this.selected.findIndex(s => s[0] === row && s[1] === index);
        if (matchIndex === -1) {
            if (!this.selected.length || this.selected[0][0] === row) {
                this.selected.push([row, index]);
            }
        } else {
            this.selected.splice(matchIndex, 1);
        }
        
        this.confirmButton.disabled = this.selected.length === 0;
        this.drawMatches();
    }

    playerMove() {
        if (!this.selected.length) return;

        const row = this.selected[0][0];
        this.piles[row] -= this.selected.length;
        this.selected = [];
        this.confirmButton.disabled = true;
        this.drawMatches();

        if (this.checkWin()) {
            this.showMessage("You Win!");
            return;
        }

        this.playerTurn = false;
        setTimeout(() => this.aiMove(), 1000);
    }

    aiMove() {
        let nimSum = this.piles.reduce((a, b) => a ^ b, 0);

        if (nimSum === 0) {
            for (let i = 0; i < this.piles.length; i++) {
                if (this.piles[i] > 0) {
                    this.piles[i]--;
                    break;
                }
            }
        } else {
            for (let i = 0; i < this.piles.length; i++) {
                const target = this.piles[i] ^ nimSum;
                if (target < this.piles[i]) {
                    this.piles[i] = target;
                    break;
                }
            }
        }

        this.drawMatches();

        if (this.checkWin()) {
            this.showMessage("AI Wins!");
            return;
        }

        this.playerTurn = true;
    }

    checkWin() {
        return this.piles.every(p => p === 0);
    }

    showMessage(message) {
        this.messageElement.textContent = message;
        setTimeout(() => {
            this.messageElement.textContent = '';
        }, 3000);
    }

    restartGame() {
        this.piles = [1, 2, 3];
        this.selected = [];
        this.playerTurn = true;
        this.confirmButton.disabled = true;
        this.messageElement.textContent = '';
        this.drawMatches();
    }
}

// initialize the game when the page loads
window.addEventListener('load', () => {
    new NimGame();
});
