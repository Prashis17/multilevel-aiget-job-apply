# Deployment

1. Set real environment variables in `.env` or your secret manager.
2. Use PostgreSQL in production:

```text
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/jobapply
```

3. Run migrations once Alembic revisions are added.
4. Start services:

```bash
docker compose up --build
```

5. Persist `browser-data`, `screenshots`, and `generated` directories on durable storage.

## Security

- Keep credentials in environment variables or a secret manager.
- Review generated emails and applications before enabling automatic mode.
- Respect job portal terms and rate limits.
- Do not bypass captcha or MFA.

