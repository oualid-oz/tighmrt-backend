"""seed_initial_roles_and_permissions

Revision ID: 6b4b5354c69c
Revises: 6bd9e081de08
Create Date: 2025-11-09 13:47:58.036377

"""
from typing import Sequence, Union, Dict, List, Any
import uuid
from datetime import datetime
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6b4b5354c69c'
down_revision: Union[str, Sequence[str], None] = '6bd9e081de08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def populate_initial_data() -> None:
    # Get database connection
    conn = op.get_bind()
    
    # Create roles
    roles = [
        {
            'id': str(uuid.uuid4()),
            'name': 'Admin',
            'code': '0000',
            'description': 'Administrator with full access',
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Manager',
            'code': '0001',
            'description': 'Manager with elevated permissions',
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'User',
            'code': '0002',
            'description': 'Regular user with basic permissions',
        }
    ]
    
    # Insert roles and store their IDs for permission assignment
    role_ids = {}
    for role in roles:
        # Insert role and get the ID
        result = conn.execute(
            sa.text(
                """
                INSERT INTO roles (id, name, code, description)
                VALUES (:id, :name, :code, :description)
                ON CONFLICT (code) DO UPDATE SET 
                    name = EXCLUDED.name,
                    description = EXCLUDED.description
                RETURNING id, code
                """
            ),
            {
                'id': role['id'],
                'name': role['name'],
                'code': role['code'],
                'description': role['description'],
            }
        ).fetchone()
        role_ids[role['code']] = role['id']
    
    # Create permissions
    permissions = [
        # User permissions (US)
        {
            'id': str(uuid.uuid4()),
            'name': 'View Users',
            'code': 'U001',  # User View
            'description': 'Can view users',
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Create Users',
            'code': 'U002',  # User Create
            'description': 'Can create users',
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Edit Users',
            'code': 'U003',  # User Edit
            'description': 'Can edit users',
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Delete Users',
            'code': 'U004',  # User Delete
            'description': 'Can delete users',
        },
        # Role permissions (RL)
        {
            'id': str(uuid.uuid4()),
            'name': 'Manage Roles',
            'code': 'R001',  # Role Manage
            'description': 'Can manage roles and permissions',
        },
        # Task permissions (TS)
        {
            'id': str(uuid.uuid4()),
            'name': 'View All Tasks',
            'code': 'T001',  # Task View
            'description': 'Can view all tasks',
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Manage All Tasks',
            'code': 'T002',  # Task Manage
            'description': 'Can manage all tasks',
        },
        # Task List permissions (TL)
        {
            'id': str(uuid.uuid4()),
            'name': 'View All Task Lists',
            'code': 'T003',  # Task List View
            'description': 'Can view all task lists',
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Manage All Task Lists',
            'code': 'T004',  # Task List Manage
            'description': 'Can manage all task lists',
        }
    ]
    
    # Insert permissions and store their IDs for role assignment
    permission_codes = {}
    for perm in permissions:
        result = conn.execute(
            sa.text("SELECT id FROM permissions WHERE code = :code"),
            {'code': perm['code']}
        ).fetchone()
        if result:
            permission_codes[perm['code']] = result[0]
            continue
        # Insert permission
        result = conn.execute(
            sa.text(
                """
                INSERT INTO permissions (id, name, code, description)
                VALUES (:id, :name, :code, :description)
                ON CONFLICT (code) DO UPDATE SET 
                    name = EXCLUDED.name,
                    description = EXCLUDED.description
                RETURNING id, code
                """
            ),
            {
                'id': perm['id'],
                'name': perm['name'],
                'code': perm['code'],
                'description': perm['description'],
            }
        ).fetchone()
        permission_codes[perm['code']] = perm['id']

    # Add admin user
    admin_user = {
        'id': str(uuid.uuid4()),
        'first_name': 'Admin',
        'last_name': 'Tighmrt',
        'phone': '0612345678',
        'email': 'admin@tighmrt.com',
        'username': 'admin',
        'hashed_password': '$2a$12$Os2apR0dE0PSMtpLoMdIkuQ.clYKe4V9MfrwMPQs9rU9p3jZ9PDJe',
        'active': True,
        'deleted': False,
        'role_code': '0000',
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
    }
    conn.execute(
        sa.text(
            """
            INSERT INTO users (id, email, hashed_password, role_id, created_at, updated_at, first_name, last_name, phone, username, active, deleted)
            VALUES (:id, :email, :hashed_password, (SELECT id FROM roles WHERE code = :role_code), :created_at, :updated_at, :first_name, :last_name, :phone, :username, :active, :deleted)
            ON CONFLICT DO NOTHING
            """
        ),
        admin_user
    )


def clear_initial_data() -> None:
    # Clear role_permissions first due to foreign key constraints
    op.execute("TRUNCATE TABLE role_permissions CASCADE")
    
    # Clear permissions and roles
    op.execute("TRUNCATE TABLE permissions CASCADE")
    op.execute("TRUNCATE TABLE roles CASCADE")


def upgrade() -> None:
    """Upgrade schema."""
    populate_initial_data()


def downgrade() -> None:
    """Downgrade schema."""
    clear_initial_data()
