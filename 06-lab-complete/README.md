# Final Production Agent (Day 12)

This is the final, production-ready AI agent from Lab 12.

## Features
- Structured JSON Logging
- Rate Limiting via Redis
- Cost Guard for LLM budget
- Stateless Design (History in Redis)
- API Key Authentication
- Multi-stage Docker build

## Running Locally

1. Create a `.env` file based on `.env.example`
2. Start the stack:
   ```bash
   docker compose up --build
   ```
3. Test Health:
   ```bash
   curl http://localhost:8000/health
   ```
4. Test API:
   ```bash
   curl -X POST http://localhost:8000/ask \
     -H "x-api-key: my-secret-key" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is Docker?"}'
   ```
