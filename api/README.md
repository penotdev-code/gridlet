# Gridlet API

Backend de gestion de compte et de sauvegarde pour Gridlet : comptes
utilisateurs (email + mot de passe), listes de mots, modèles et favoris.

- **FastAPI** + **SQLAlchemy 2.0 (async)** + **Pydantic v2**
- **Postgres** en production (asyncpg), **SQLite** par défaut en dev (zéro install)
- Auth **email/mot de passe** : hash bcrypt + **JWT** bearer

## Démarrer en local (SQLite, zéro install)

```bash
cd api
uv sync                       # crée .venv et installe les dépendances
uv run uvicorn app.main:app --reload --port 8000
```

- API : http://localhost:8000
- Docs interactives (Swagger) : http://localhost:8000/docs

Les tables sont créées automatiquement au démarrage (pratique en dev).

## Tests

```bash
cd api
uv run pytest
```

## Postgres (dev avec Docker, ou prod)

```bash
docker compose up -d db        # lance Postgres en local
cp .env.example .env           # puis décommentez la ligne DATABASE_URL Postgres
uv run uvicorn app.main:app --reload --port 8000
```

En production, définissez `DATABASE_URL` (DSN `postgresql+asyncpg://…`) et un
`JWT_SECRET` long et aléatoire, et appliquez les migrations Alembic plutôt que
la création automatique des tables.

## Endpoints

| Méthode | Route | Description |
| --- | --- | --- |
| POST | `/auth/register` | Créer un compte → token |
| POST | `/auth/login` | Connexion → token |
| GET | `/auth/me` | Utilisateur courant |
| GET/POST | `/lists` | Lister / créer des listes (`?template=true` pour les modèles) |
| GET/PUT/DELETE | `/lists/{id}` | Détail / mise à jour / suppression |
| GET/POST | `/favorites` | Lister / enregistrer des grilles favorites |
| DELETE | `/favorites/{id}` | Supprimer un favori |

Toutes les routes (hors `/auth/register` et `/auth/login`) requièrent un header
`Authorization: Bearer <token>`.

## Migrations (Alembic)

La config Alembic est fournie (`alembic.ini`, `alembic/`). Une fois branché sur
votre Postgres :

```bash
uv run alembic revision --autogenerate -m "init"
uv run alembic upgrade head
```

## Déploiement

Ce backend ne peut pas être hébergé sur GitHub Pages (statique). Cibles
adaptées : Fly.io, Railway, Render… avec un Postgres managé.
