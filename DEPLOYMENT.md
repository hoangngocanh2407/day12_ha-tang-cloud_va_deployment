# Deployment Information

## Public URL
https://precious-spontaneity-production-66dd.up.railway.app

## Platform
Railway

## Test Commands

### Health Check
```bash
curl https://precious-spontaneity-production-66dd.up.railway.app/health
# Expected: {"status": "ok"}
```

### API Test (with authentication)
```bash
curl -X POST https://precious-spontaneity-production-66dd.up.railway.app/ask \
  -H "X-API-Key: my-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Docker?"}'
```

## Environment Variables Set
- PORT
- REDIS_URL
- AGENT_API_KEY
- LOG_LEVEL

## Screenshots
- [Deployment dashboard](screenshots/dashboard.png)
- [Service running](screenshots/running.png)
- [Test results](screenshots/test.png)
