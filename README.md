# 🎮 AysieElf Games Plan

## 📚 Technical Stack
- Frontend: React.js + Phaser.js (+ JavaScript Bridge?)
- Backend: Python FastAPI
- Database: PostgreSQL
- ORM: SQLAlchemy
- Authentication: JWT tokens
- Deployment: Heroku
- WebSocket: FastAPI WebSockets
- State Management: Redis (for multiplayer sessions)

## Current progress
[▓░░░░░░░░░░░░░░░░░░░] 0/8%
- [ ] [Initial Setup & Early Deployment (deadline: 19.01.2025)](#1-initial-setup--early-deployment-1-week)
- [ ] [Backend Foundation (deadline: 02.02.2025)](#2-backend-foundation-2-weeks)
- [ ] [Social Features (deadline: 16.02.2025)](#3-social-features-2-weeks)
- [ ] [Game Integration Base (deadline: 02.03.2025)](#4-game-integration-base-2-weeks)
- [ ] [First Game Port - Sleepy Fox (deadline: 23.03.2025)](#5-first-game-port---sleepy-fox-3-weeks)
- [ ] [Multiplayer Foundation (deadline: 06.04.2025)](#6-multiplayer-foundation-2-седмици)
- [ ] [UI/UX Development (deadline: 20.04.2025)](#7-uiux-development-2-седмици)
- [ ] [Polish & Launch (deadline: 27.04.2025)](#8-polish--launch-1-week)

## 🗺️ Project Phases

### 1️⃣ Initial Setup & Early Deployment (1 week)
- [x] Choose technical stack
- [x] Create GitHub repository
- [x] Basic project structure:
  ```
  aysieelf-games/
  ├── frontend/          
  │   └── coming-soon/   # Initial landing page
  ├── backend/           
  │   └── health-check/  # Basic endpoint
  └── docs/             
  ```
- [ ] Venv, Lint
- [ ] Healthcheck endpoint
- [ ] Minimal deployments

### 2️⃣ Backend Foundation (2 weeks)
- [ ] FastAPI base structure
- [ ] Database setup & migrations:
  ```
  users
    - id, username, email, avatar
    - created_at, last_login
  
  games
    - id, title, description
    - is_multiplayer, player_count
    
  favorites
    - user_id, game_id, added_at
    
  friendships
    - user_id, friend_id
    - created_at, status
    
  game_activities
    - user_id, game_id
    - played_at, duration
  ```
- [ ] Core API endpoints:
  ```
  /api/v1/
  ├── auth/
  ├── games/
  │   ├── list
  │   └── {game_id}/details
  └── users/
      └── me/
  ```

### 3️⃣ Social Features (2 weeks)
- [ ] User profiles
- [ ] Friend system
- [ ] Favorites management
- [ ] Activity feed
- [ ] Real-time notifications

### 4️⃣ Game Integration Base (2 weeks)
- [ ] Phaser.js setup
- [ ] Game wrapper component
- [ ] Save states
- [ ] Activity tracking

### 5️⃣ First Game Port - Sleepy Fox (3 weeks)
- [ ] Single player mode
- [ ] Local multiplayer
- [ ] In-game leaderboard
- [ ] Save progress

### 6️⃣ Multiplayer Foundation (2 weeks)
- [ ] WebSocket setup
- [ ] Game room system
- [ ] Player matching
- [ ] Connection handling
- [ ] State synchronization

### 7️⃣ UI/UX Development (2 weeks)
- [ ] Home page with favorites
- [ ] Friend activity feed
- [ ] Game lobby system
- [ ] Profile customization
- [ ] Responsive design

### 8️⃣ Polish & Launch (1 week)
- [ ] Performance optimization
- [ ] Documentation
- [ ] Testing
- [ ] Deployment guide

## 📈 Future Phases
- Additional games (Snake, Breakout...)
- Achievement system
