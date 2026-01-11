"""
Migration script to create the user table
"""

def upgrade():
    """
    Create the user table with required columns
    """
    print("""
    CREATE TABLE user (
        id VARCHAR(255) PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    """)


def downgrade():
    """
    Drop the user table
    """
    print("DROP TABLE user;")