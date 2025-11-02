# Repository Guidelines

## Project Structure & Module Organization
- Django backend lives under `files/`, `users/`, `rbac/`, `actions/`, `identity_providers/`, and `cms/` (settings, URLs, Celery config). Shared templates and static assets sit in `templates/` and `static/`.
- Media processing helpers and Celery tasks are primarily in `files/helpers.py` and `files/tasks.py`. Upload logic resides in `uploader/`.
- The React frontend, tooling, and build config are inside `frontend/` with supplemental packages in `frontend-tools/`. Generated bundles must be copied to `static/`.
- Automated tests are centralised in `tests/` with app-specific tests colocated under each app’s `tests` package.

## Build, Test, and Development Commands
- `docker compose -f docker-compose-dev.yaml up` — start the full dev stack (Postgres, Redis, Django, Celery, React dev server).
- `make build-frontend` — build production frontend assets, copy them into `static/`, and restart the Django container.
- `make test` (or `docker compose -f docker-compose-dev.yaml exec --env TESTING=True -T web pytest`) — run the pytest suite inside the web container.
- `pre-commit run --all-files` — apply Black, isort, and Flake8 checks before committing.

## Frontend Development Workflow
### Development Modes
- **Frontend Dev Server (http://localhost:8088)**:
  - Runs Webpack Dev Server with Hot Module Replacement (HMR)
  - Automatically recompiles on file changes
  - **⚠️ Does NOT include Django translations** - translations are only available through Django backend
  - Use for rapid CSS/SCSS development and testing component logic

- **Django Backend (http://localhost:8080)**:
  - Serves Django templates with embedded React components
  - Includes full translation support via `window.TRANSLATION` object
  - Uses pre-built static files from `static/` directory
  - **This is the production-like environment** - always test here before committing

### When to Run `make build-frontend`
**⚠️ IMPORTANT**: In development mode, Django uses pre-built files from `static/`, NOT the dev server's live compilation.

**You MUST run `make build-frontend` after**:
- Modifying React components (`.jsx`, `.tsx` files)
- Changing JavaScript logic
- Adding/modifying translation strings in frontend code
- Any changes that affect the compiled JavaScript output

**You DON'T need to run it for**:
- CSS/SCSS changes (these are hot-reloaded by the dev server)
- Django template changes
- Python backend changes
- Adding translations to `files/frontend_translations/*.py` (just restart web container)

### Translation System
- **Backend translations**: Located in `files/frontend_translations/zh_hans.py` (and other language files)
- **Frontend usage**: Use `translateString('English text')` helper function in React components
- **How it works**:
  1. Django passes translations via `window.TRANSLATION` object in templates
  2. React components call `translateString()` to get translated text
  3. Translations are loaded from `files.context_processors.stuff` context processor
- **Testing translations**: Always use http://localhost:8080 (Django backend), not http://localhost:8088 (dev server)

### Common Issues
1. **"I modified React code but don't see changes on http://localhost:8080"**
   - Solution: Run `make build-frontend` to rebuild and copy files to `static/`

2. **"Translations don't appear in the browser"**
   - Check you're accessing http://localhost:8080 (not 8088)
   - Verify translation exists in `files/frontend_translations/zh_hans.py`
   - Restart web container: `docker compose -f docker-compose-dev.yaml restart web`
   - Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)

3. **"CSS changes don't show up"**
   - CSS changes should hot-reload automatically via dev server
   - If not working, check frontend container logs: `docker compose -f docker-compose-dev.yaml logs frontend`

## Coding Style & Naming Conventions
- Python: Black (200-char lines, no string normalization) plus Flake8 (`max-line-length=119`) and isort with Black profile. Follow Django conventions for modules and snake_case for identifiers.
- Frontend: Prettier (`printWidth: 120`, single quotes, 4-space indentation) and TypeScript/React best practices; keep components in PascalCase.
- Templates/Static: store overrides in `templates/cms/` and `static/css|js/`, matching existing naming patterns.

## Testing Guidelines
- Tests use Pytest with `pytest-django`; test modules begin with `test_` and should live alongside related code or in `tests/`.
- Use `TESTING=True` env when invoking Django-managed commands so Celery runs tasks eagerly.
- Aim to cover new business logic with unit tests; integration tests can exercise API endpoints via DRF test client.

## Commit & Pull Request Guidelines
- Write imperative, scoped commit messages (e.g., `Add RBAC category mapping helper`). Squash fix-up commits before submission.
- PRs should describe the problem, highlight key changes, list test commands (e.g., `make test`), and attach screenshots for UI updates.
- Link relevant GitHub issues and call out any configuration or migration steps required for reviewers.

## Security & Configuration Tips
- Update secrets (`SECRET_KEY`, admin passwords) and domain settings in `cms/local_settings.py` or environment variables before deployment.
- Keep `media_files/` and `postgres_data/` on persistent storage; monitor disk usage during heavy transcoding.
- When enabling Whisper or SAML, switch to the `mediacms/mediacms:full` image and review related settings in `cms/settings.py`.
请全程保持中文交流沟通！