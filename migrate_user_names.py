"""
Migration script to split full_name into first_name and last_name
Run this script once to migrate existing data
"""
from app import create_app
from models import db
import sqlalchemy as sa

def migrate_user_names():
    app = create_app()
    with app.app_context():
        # Check if columns exist
        inspector = sa.inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('user')]

        print(f"Current columns: {columns}")

        # If old schema, migrate
        if 'full_name' in columns and 'first_name' not in columns:
            print("Migrating from full_name to first_name/last_name...")

            # Add new columns
            with db.engine.connect() as conn:
                conn.execute(sa.text("ALTER TABLE \"user\" ADD COLUMN first_name VARCHAR(50)"))
                conn.execute(sa.text("ALTER TABLE \"user\" ADD COLUMN last_name VARCHAR(50)"))
                conn.commit()

            # Migrate existing data
            users = db.session.execute(sa.text("SELECT id, full_name FROM \"user\"")).fetchall()

            for user_id, full_name in users:
                # Split full_name into first and last
                parts = full_name.strip().split(maxsplit=1)
                first_name = parts[0] if parts else 'Unknown'
                last_name = parts[1] if len(parts) > 1 else ''

                db.session.execute(
                    sa.text("UPDATE \"user\" SET first_name = :first, last_name = :last WHERE id = :id"),
                    {'first': first_name, 'last': last_name, 'id': user_id}
                )

            db.session.commit()

            # Drop old column
            with db.engine.connect() as conn:
                conn.execute(sa.text("ALTER TABLE \"user\" DROP COLUMN full_name"))
                conn.commit()

            # Make new columns NOT NULL
            with db.engine.connect() as conn:
                conn.execute(sa.text("ALTER TABLE \"user\" ALTER COLUMN first_name SET NOT NULL"))
                conn.execute(sa.text("ALTER TABLE \"user\" ALTER COLUMN last_name SET NOT NULL"))
                conn.commit()

            print("✓ Migration complete!")

        elif 'first_name' in columns and 'last_name' in columns:
            print("✓ Database already migrated (first_name and last_name exist)")

        else:
            print("Creating new database schema...")
            db.create_all()
            print("✓ Tables created with new schema")

if __name__ == '__main__':
    migrate_user_names()
