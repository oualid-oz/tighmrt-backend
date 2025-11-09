# Tighmrt Backend

## Database Migrations with Alembic

This project uses [Alembic](https://alembic.sqlalchemy.org/) for database migrations. Alembic is a lightweight database migration tool for SQLAlchemy.

### Setup

1. Ensure you have all dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure your database connection in `alembic.ini`:
   ```ini
   sqlalchemy.url = driver://user:password@localhost/dbname
   ```

### Creating Migrations

To create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Applying Migrations

To apply all pending migrations:
```bash
albemic upgrade head
```

### Common Commands

- Create a new migration: `alembic revision --autogenerate -m "your message"`
- Apply all pending migrations: `alembic upgrade head`
- Revert last migration: `alembic downgrade -1`
- Show current revision: `alembic current`
- Show migration history: `alembic history`

### Migration Workflow

1. Make changes to your SQLAlchemy models
2. Generate a migration: `alembic revision --autogenerate -m "your changes"`
3. Review the generated migration file in `alembic/versions/`
4. Apply the migration: `alembic upgrade head`

### Troubleshooting

- If you encounter issues with autogenerate, try running `alembic stamp head` first
- Always test migrations in a development environment before applying to production
- Check the `alembic.ini` file for correct database connection settings
