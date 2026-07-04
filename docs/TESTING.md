# Testing Strategy

- Unit test scoring, deduplication, config parsing, and provider adapters.
- Integration test FastAPI endpoints with a temporary SQLite database.
- Browser tests should use Playwright traces and test career-page fixtures.
- Production portal adapters should have replayable HTML fixtures to avoid brittle live tests.

Run:

```bash
pytest
ruff check .
```

