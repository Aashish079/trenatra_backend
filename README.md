# Tenatra Backend

FastAPI backend with authentication.

## Setup

1. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
```

2. Install dependencies:
```bash
pip install -e .
```

3. Copy sample.env to .env and configure:
```bash
cp sample.env .env
```

4. Run the development server:
```bash
fastapi dev app/main.py
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login with Basic Auth (returns session token)
- `GET /auth/me` - Get current user (requires Bearer token)
