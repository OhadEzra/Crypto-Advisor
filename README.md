# AI Crypto Advisor - Moveo Coding Task

A personalized crypto investor dashboard. Users register, complete a short onboarding quiz, and receive a tailored dashboard with market news, coin prices, AI insight, and a fun crypto meme. Each dashboard section supports thumbs up/down feedback, stored in the database for future recommendation improvements.

## Tech Stack

### Frontend
- React
- TypeScript
- Vite
- Tailwind CSS
- React Router
- Axios

### Backend
- FastAPI
- SQLite with SQLAlchemy
- JWT authentication
- CoinGecko API for prices
- CryptoCompare news API as a free market-news source
- OpenRouter AI integration with safe fallback

## Main Features

- Signup and login with JWT authentication
- First-login onboarding quiz
- User preferences stored in DB
- Personalized dashboard based on user profile
- Coin prices with live API + fallback
- Market news with live API + fallback
- AI insight of the day using OpenRouter + fallback
- Dynamic crypto meme
- Voting system for every section
- Feedback stored for future model improvements

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

## Local Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

Health check:

```bash
http://localhost:8000/health
```

API docs:

```bash
http://localhost:8000/docs
```

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

## Environment Variables

Backend `.env`:

```env
SECRET_KEY=replace-with-a-long-random-secret
OPENROUTER_API_KEY=
OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct:free
FRONTEND_ORIGIN=http://localhost:5173
DATABASE_URL=sqlite:///./crypto_advisor.db
```

Frontend `.env`:

```env
VITE_API_URL=http://localhost:8000
```

The app works even without an AI API key by using a local fallback insight generator.

## Database Access

The app uses SQLite by default. The database file is created automatically in the backend directory:

```txt
backend/crypto_advisor.db
```

Useful tables:

- `users`
- `preferences`
- `votes`

You can inspect it with any SQLite browser or with the command line:

```bash
sqlite3 crypto_advisor.db
.tables
SELECT * FROM users;
SELECT * FROM preferences;
SELECT * FROM votes;
```

## Deployment Plan

Recommended free deployment:

- Frontend: Vercel or Netlify
- Backend: Render or Railway
- DB: SQLite for simple demo deployment, or PostgreSQL for production-style deployment

When deploying, set:

```env
FRONTEND_ORIGIN=https://your-frontend-url.vercel.app
VITE_API_URL=https://your-backend-url.onrender.com
SECRET_KEY=secure-production-secret
```

## Future Training / Feedback Improvement Proposal

The current app stores explicit user feedback in the `votes` table. Each vote includes:

- user ID
- dashboard section
- item ID
- vote value: `1` for thumbs up, `-1` for thumbs down
- timestamp

A future recommendation-training process could work like this:

1. Collect user votes from dashboard sections.
2. Aggregate feedback by user profile, asset interest, investor type, and content type.
3. Assign higher ranking scores to content patterns that received positive feedback.
4. Reduce the ranking of sections, sources, or topics that repeatedly received negative feedback.
5. Periodically build a lightweight preference profile per user.
6. Use this profile in the AI prompt and content-ranking layer before displaying the next dashboard.

This would not require immediately training a full model. A first production step could be a recommendation scoring layer. Later, the stored feedback could be exported and used for supervised fine-tuning or reinforcement learning from human feedback style optimization.

## Notes

This project is educational and does not provide financial advice.
