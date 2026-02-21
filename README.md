# ⚽ Football Club Logo Guessing Game

A production-ready backend application featuring a football club logo guessing game with progressive blur mechanics. Built with clean architecture principles and best practices.

## 🎮 Game Overview

Test your football knowledge by identifying club logos through increasingly clearer images. Each game consists of 10 randomly selected logos, with 5 attempts per logo. The faster you guess correctly, the more points you earn!

### Scoring System
- **1st attempt**: 10 points
- **2nd attempt**: 8 points
- **3rd attempt**: 7 points
- **4th attempt**: 6 points
- **5th attempt**: 5 points
- **No correct guess**: 0 points

## 🛠️ Technology Stack

### Backend
- **Python 3.11+**
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy 2.0** - SQL toolkit and ORM
- **SQLite** - Lightweight database
- **Pydantic** - Data validation
- **Jinja2** - Template engine

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling with modern gradients and animations
- **Vanilla JavaScript** - Game logic and API communication
- **Fetch API** - RESTful communication

## 📁 Project Structure

```
football-logo-game/
├── api/
│   └── game_router.py          # API endpoints
├── core/
│   ├── config.py               # Application settings
│   └── database.py             # Database configuration
├── models/
│   ├── club.py                 # Club database model
│   └── game.py                 # Game & GameRound models
├── schemas/
│   └── game.py                 # Pydantic schemas
├── services/
│   └── game_service.py         # Business logic
├── static/
│   ├── css/
│   │   └── style.css           # Application styles
│   ├── js/
│   │   └── game.js             # Frontend logic
│   └── logos/                  # Club logo images
├── templates/
│   └── index.html              # Main HTML template
├── main.py                     # FastAPI application
├── seed_data.py                # Database seeding script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Step 1: Clone or Download
```bash
git clone <your-repo-url>
cd football-logo-game
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Add Logo Images
Place football club logo images in the `static/logos/` directory. The seeding script expects these files:

- `manchester_united.png`
- `liverpool.png`
- `barcelona.png`
- `real_madrid.png`
- `bayern_munich.png`
- `juventus.png`
- `psg.png`
- `chelsea.png`
- `arsenal.png`
- `manchester_city.png`
- `ac_milan.png`
- `inter_milan.png`
- `ajax.png`
- `borussia_dortmund.png`
- `atletico_madrid.png`
- `tottenham.png`
- `benfica.png`
- `porto.png`
- `celtic.png`
- `rangers.png`

**Note**: You can find free logo images from sources like Wikipedia Commons or official club websites. Ensure you have proper rights to use the images.

### Step 5: Seed Database
```bash
python seed_data.py
```

Expected output:
```
Creating database tables...
Seeding database...
Successfully seeded 20 clubs!
Seeding complete!
```

### Step 6: Run Application
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at: **http://localhost:8000**

## 🎯 How to Play

1. **Start Game**: Click "Start Game" button
2. **View Logo**: See a heavily blurred football club logo
3. **Make Guess**: Type the club name and submit
4. **Get Feedback**: 
   - ✓ Correct guess → Earn points and move to next logo
   - ✗ Incorrect guess → Logo becomes clearer, try again
5. **Complete Round**: After 5 attempts or correct guess, move to next logo
6. **Finish Game**: Complete all 10 logos to see your final score

## 🔌 API Endpoints

### Start New Game
```http
POST /api/game/start
```
**Response**: `{ game_id, message, total_logos }`

### Get Current Logo
```http
GET /api/game/current?game_id={id}
```
**Response**: Current logo data with blur level (doesn't expose correct answer)

### Submit Guess
```http
POST /api/game/guess
Body: { game_id, guess }
```
**Response**: Feedback on guess correctness and updated game state

### Get Final Results
```http
GET /api/game/result?game_id={id}
```
**Response**: Complete game summary with all rounds and final score

## 🏗️ Architecture Highlights

### Clean Architecture
- **Separation of Concerns**: Business logic separated from route handlers
- **Service Layer**: All game logic in `GameService` class
- **Database Models**: SQLAlchemy ORM models
- **Schemas**: Pydantic validation for API requests/responses
- **Dependency Injection**: Database sessions via FastAPI dependencies

### Best Practices
- ✅ Input validation and normalization
- ✅ Proper error handling with HTTP status codes
- ✅ RESTful API design
- ✅ No business logic in route handlers
- ✅ Type hints throughout codebase
- ✅ Configurable settings via Pydantic
- ✅ Database session management
- ✅ Clean, readable code structure

## 🧪 Development

### Adding New Clubs
Edit `seed_data.py` and add entries to `clubs_data`:
```python
{"name": "New Club", "logo_path": "/static/logos/new_club.png"}
```

### Modifying Game Rules
Edit `core/config.py`:
```python
LOGOS_PER_GAME = 10      # Number of logos per game
MAX_ATTEMPTS = 5          # Attempts per logo
POINTS_MAPPING = {...}    # Scoring system
BLUR_LEVELS = {...}       # Blur progression
```

### Running in Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📊 Database Schema

### Tables
1. **clubs**: Football club information
   - id, name, logo_path

2. **games**: Game sessions
   - id, current_logo_index, total_score, finished, created_at

3. **game_rounds**: Individual rounds within games
   - id, game_id, club_id, attempts_used, guessed_correctly, points_earned


---

**Enjoy the game! ⚽**