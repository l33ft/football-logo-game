// Game state
let gameState = {
    gameId: null,
    currentScore: 0,
    isProcessing: false
};

// DOM elements
const startScreen = document.getElementById('startScreen');
const gameScreen = document.getElementById('gameScreen');
const resultsScreen = document.getElementById('resultsScreen');

const startButton = document.getElementById('startButton');
const submitGuess = document.getElementById('submitGuess');
const nextButton = document.getElementById('nextButton');
const playAgainButton = document.getElementById('playAgainButton');

const guessInput = document.getElementById('guessInput');
const logoImage = document.getElementById('logoImage');
const logoCounter = document.getElementById('logoCounter');
const currentScore = document.getElementById('currentScore');
const attemptsLeft = document.getElementById('attemptsLeft');
const feedback = document.getElementById('feedback');
const finalScore = document.getElementById('finalScore');
const roundsDetails = document.getElementById('roundsDetails');

// API base URL
const API_BASE = '/api';

// Event listeners
startButton.addEventListener('click', startNewGame);
submitGuess.addEventListener('click', submitGuessHandler);
nextButton.addEventListener('click', loadCurrentLogo);
playAgainButton.addEventListener('click', resetGame);

guessInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !gameState.isProcessing) {
        submitGuessHandler();
    }
});

// Start new game
async function startNewGame() {
    try {
        startButton.disabled = true;
        startButton.textContent = 'Starting...';

        const response = await fetch(`${API_BASE}/game/start`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Failed to start game');
        }

        const data = await response.json();
        gameState.gameId = data.game_id;
        gameState.currentScore = 0;

        // Switch to game screen
        showScreen('game');
        loadCurrentLogo();

    } catch (error) {
        console.error('Error starting game:', error);
        alert('Failed to start game. Please try again.');
        startButton.disabled = false;
        startButton.textContent = 'Start Game';
    }
}

// Load current logo
async function loadCurrentLogo() {
    try {
        const response = await fetch(`${API_BASE}/game/current?game_id=${gameState.gameId}`);

        if (!response.ok) {
            throw new Error('Failed to load logo');
        }

        const data = await response.json();

        // Update UI
        logoImage.src = data.logo_path;
        logoImage.style.filter = `blur(${data.blur_level}px)`;
        logoCounter.textContent = `${data.logo_index} / ${data.total_logos}`;
        currentScore.textContent = data.current_score;
        attemptsLeft.textContent = data.attempts_left;
        gameState.currentScore = data.current_score;

        // Reset input and feedback
        guessInput.value = '';
        guessInput.disabled = false;
        guessInput.focus();
        feedback.className = 'feedback hidden';
        feedback.textContent = '';

        // Hide next button, enable submit
        nextButton.classList.add('hidden');
        submitGuess.disabled = false;

    } catch (error) {
        console.error('Error loading logo:', error);
        alert('Failed to load logo. Please refresh the page.');
    }
}

// Submit guess
async function submitGuessHandler() {
    const guess = guessInput.value.trim();

    if (!guess) {
        return;
    }

    if (gameState.isProcessing) {
        return;
    }

    try {
        gameState.isProcessing = true;
        submitGuess.disabled = true;

        const response = await fetch(`${API_BASE}/game/guess`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                game_id: gameState.gameId,
                guess: guess
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to submit guess');
        }

        const data = await response.json();

        // Update UI
        currentScore.textContent = data.current_score;
        attemptsLeft.textContent = data.attempts_left;
        gameState.currentScore = data.current_score;

        // Update blur
        logoImage.style.filter = `blur(${data.blur_level}px)`;

        // Show feedback
        feedback.classList.remove('hidden');

        if (data.correct) {
            feedback.className = 'feedback correct';
            feedback.textContent = `✓ Correct! +${data.points_earned} points`;
            guessInput.disabled = true;

            if (data.game_finished) {
                // Game is complete
                setTimeout(() => showResults(), 1500);
            } else {
                // Show next button
                nextButton.classList.remove('hidden');
            }

        } else if (data.finished_round) {
            // Out of attempts
            feedback.className = 'feedback revealed';
            feedback.textContent = `✗ Out of attempts! The answer was: ${data.correct_answer}`;
            guessInput.disabled = true;

            if (data.game_finished) {
                // Game is complete
                setTimeout(() => showResults(), 2000);
            } else {
                // Show next button
                nextButton.classList.remove('hidden');
            }

        } else {
            // Incorrect but more attempts available
            feedback.className = 'feedback incorrect';
            feedback.textContent = `✗ Incorrect. Try again! (${data.attempts_left} attempts left)`;
            guessInput.value = '';
            guessInput.focus();
            submitGuess.disabled = false;
        }

    } catch (error) {
        console.error('Error submitting guess:', error);
        feedback.className = 'feedback incorrect';
        feedback.classList.remove('hidden');
        feedback.textContent = error.message;
        submitGuess.disabled = false;
    } finally {
        gameState.isProcessing = false;
    }
}

// Show results
async function showResults() {
    try {
        const response = await fetch(`${API_BASE}/game/result?game_id=${gameState.gameId}`);

        if (!response.ok) {
            throw new Error('Failed to load results');
        }

        const data = await response.json();

        // Update final score
        finalScore.textContent = data.total_score;

        // Build rounds details
        roundsDetails.innerHTML = '';

        data.rounds.forEach((round, index) => {
            const roundDiv = document.createElement('div');
            roundDiv.className = 'round-item';

            const pointsClass = round.points_earned > 0 ? '' : 'zero';
            const statusClass = round.guessed_correctly ? 'status-correct' : 'status-wrong';
            const statusText = round.guessed_correctly
                ? `✓ Guessed in ${round.attempts_used} attempt${round.attempts_used > 1 ? 's' : ''}`
                : `✗ Not guessed (${round.attempts_used} attempts)`;

            roundDiv.innerHTML = `
                <img src="${round.logo_path}" alt="${round.club_name}" class="round-logo">
                <div class="round-info">
                    <div class="round-name">${round.club_name}</div>
                    <div class="round-details ${statusClass}">${statusText}</div>
                </div>
                <div class="round-points ${pointsClass}">+${round.points_earned}</div>
            `;

            roundsDetails.appendChild(roundDiv);
        });

        // Show results screen
        showScreen('results');

    } catch (error) {
        console.error('Error loading results:', error);
        alert('Failed to load results. Please try again.');
    }
}

// Reset game
function resetGame() {
    gameState = {
        gameId: null,
        currentScore: 0,
        isProcessing: false
    };

    startButton.disabled = false;
    startButton.textContent = 'Start Game';

    showScreen('start');
}

// Show specific screen
function showScreen(screen) {
    startScreen.classList.add('hidden');
    gameScreen.classList.add('hidden');
    resultsScreen.classList.add('hidden');

    switch(screen) {
        case 'start':
            startScreen.classList.remove('hidden');
            break;
        case 'game':
            gameScreen.classList.remove('hidden');
            break;
        case 'results':
            resultsScreen.classList.remove('hidden');
            break;
    }
}