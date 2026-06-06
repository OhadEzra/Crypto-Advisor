# AI Crypto Advisor - Moveo Coding Task

A personalized crypto investor dashboard. Users register, complete a short onboarding quiz, and receive a tailored dashboard with market news, coin prices, AI insights, and a fun crypto meme. Each dashboard section supports thumbs up/down feedback, which is stored in the database and can be used to improve future recommendations.

---

## Live Demo

### Frontend

https://crypto-advisor-one.vercel.app

### Backend Health Check

https://crypto-advisor-api.onrender.com/health

### GitHub Repository

https://github.com/OhadEzra/Crypto-Advisor

---

## Dashboard Overview

After onboarding, users receive a personalized dashboard containing:

* Coin Prices
* Market News
* AI Insight of the Day
* Fun Crypto Meme
* Personalized Watchlist
* AI Recommendations
* Market Sentiment Analysis
* Portfolio Health Score
* Risk Profile Assessment
* Voting and Feedback Collection

---

## Tech Stack

### Frontend

* React
* TypeScript
* Vite
* Tailwind CSS
* React Router
* Axios

### Backend

* FastAPI
* SQLite with SQLAlchemy
* JWT Authentication
* CoinGecko API for crypto prices
* CryptoCompare API for market news
* OpenRouter AI integration with safe fallback generation

---

## Main Features

* Signup and login with JWT authentication
* First-login onboarding experience
* User preferences stored in database
* Personalized dashboard based on onboarding profile
* Live coin prices with fallback support
* Live crypto news with fallback support
* AI Insight of the Day using OpenRouter
* Dynamic crypto meme section
* Personalized watchlist management
* AI-generated recommendations
* Market sentiment analysis
* Portfolio health scoring
* Risk profile assessment
* Voting system for every dashboard section
* Feedback stored for future recommendation improvements

---

## Project Structure

```txt
backend/
  app/
    routers/
      auth.py
      users.py
      dashboard.py
    services/
      ai.py
      coingecko.py
      news.py
      memes.py
    database.py
    dependencies.py
    main.py
    models.py
    schemas.py
    security.py

frontend/
  src/
    components/
    pages/
    services/
```

---

## Local Setup

### Backend

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env

uvicorn app.main:app --reload --port 8000
```

Health Check:

```bash
http://localhost:8000/health
```

API Documentation:

```bash
http://localhost:8000/docs
```

---

### Frontend

```bash
cd frontend

npm install

cp .env.example .env

npm run dev
```

Open:

```bash
http://localhost:5173
```

---

## Environment Variables

### Backend (.env)

```env
SECRET_KEY=replace-with-a-long-random-secret
OPENROUTER_API_KEY=
OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct:free
FRONTEND_ORIGIN=http://localhost:5173
DATABASE_URL=sqlite:///./crypto_advisor.db
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
```

The application can operate without an AI API key by using a local fallback insight generator.

---

## Database Access

The application uses SQLite by default.

Database file:

```txt
backend/crypto_advisor.db
```

Main tables:

* users
* preferences
* votes

Useful commands:

```bash
sqlite3 crypto_advisor.db

.tables

SELECT * FROM users;

SELECT * FROM preferences;

SELECT * FROM votes;
```

---



## AI Tools Usage Summary

During development I used several AI-assisted development tools as part of the engineering process, including:

- ChatGPT for architecture discussions, debugging assistance, documentation, and implementation planning.
- GitHub Copilot for code completion and development productivity.
- Cursor AI for code navigation, refactoring suggestions, and rapid iteration.
- OpenRouter models for testing and validating AI-generated dashboard insights.

AI tools were primarily used to accelerate research, troubleshooting, brainstorming, and development workflows.

All final implementation decisions, code integration, testing, deployment, debugging, and production configuration were performed manually.

---

## Future Training / Feedback Improvement Proposal

The current application stores explicit user feedback in the `votes` table.

Each vote contains:

* User ID
* Dashboard section
* Item ID
* Vote value (`1` for thumbs up, `-1` for thumbs down)
* Timestamp

A future recommendation-training workflow could be:

1. Collect user feedback from dashboard interactions.
2. Aggregate votes by investor type, preferred assets, and content interests.
3. Increase ranking scores for content patterns that receive positive feedback.
4. Reduce ranking scores for content patterns that repeatedly receive negative feedback.
5. Build lightweight user preference profiles over time.
6. Use those profiles when generating AI prompts and ranking dashboard content.

This approach enables personalization without immediately training a custom machine learning model.

In later stages, collected feedback could be exported for supervised fine-tuning or reinforcement-learning-based optimization.

---

## Deployment

### Frontend

* Vercel

### Backend

* Render

### Database

* SQLite

Production environment variables:

```env
FRONTEND_ORIGIN=https://crypto-advisor-one.vercel.app
VITE_API_URL=https://crypto-advisor-api.onrender.com
SECRET_KEY=secure-production-secret
```

---

## Notes

This project was built as part of the Moveo AI Crypto Advisor coding assignment.

The application is intended for educational and demonstration purposes only and does not provide financial advice.
