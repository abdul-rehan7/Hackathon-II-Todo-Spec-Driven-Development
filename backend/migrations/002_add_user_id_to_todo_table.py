"""
Migration script to add user_id column to the todo table
"""

def upgrade():
    """
    Add the user_id column to the todo table with a foreign key constraint
    """
    print("""
    ALTER TABLE todo ADD COLUMN user_id VARCHAR(255) NOT NULL DEFAULT 'temp-user-id';

    -- Add foreign key constraint
    ALTER TABLE todo
    ADD CONSTRAINT fk_todo_user
    FOREIGN KEY (user_id) REFERENCES user(id);

    -- Create index for better performance
    CREATE INDEX idx_todo_user_id ON todo(user_id);
    """)


def downgrade():
    """
    Remove the user_id column from the todo table
    """
    print("""
    ALTER TABLE todo DROP FOREIGN KEY fk_todo_user;
    ALTER TABLE todo DROP COLUMN user_id;
    """)