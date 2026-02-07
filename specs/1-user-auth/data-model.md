# Data Model: User Authentication

**Feature**: User Authentication with better-auth.com
**Date**: 2026-01-10
**Branch**: 1-user-auth

## Entities

### User
**Description**: Represents registered users in the system

**Fields**:
- id: Unique identifier for the user (UUID/string)
- email: User's email address (string, unique, required)
- password: Hashed password (managed by better-auth, secure)
- created_at: Timestamp when account was created (datetime)

**Validation Rules**:
- Email must be valid email format
- Email must be unique across all users
- Password must meet security requirements (handled by better-auth)
- All required fields must be present during registration

**Relationships**:
- One-to-Many: User → Todo (one user can have many todos)

### Todo
**Description**: Represents individual todo items linked to specific users

**Fields**:
- id: Unique identifier for the todo item (UUID/string)
- title: Title of the todo item (string, required)
- completed: Status of the todo (boolean, default: false)
- user_id: Foreign key linking to the owning user (UUID/string, required)
- created_at: Timestamp when todo was created (datetime)
- updated_at: Timestamp when todo was last modified (datetime)

**Validation Rules**:
- Title must not be empty
- user_id must reference an existing user
- Todo operations must be performed by the owning user only

**Relationships**:
- Many-to-One: Todo → User (many todos belong to one user)

## State Transitions

### User State Transitions
- Unregistered → Registered (upon successful signup)
- Registered → Authenticated (upon successful login)
- Authenticated → Unauthenticated (upon logout)

### Todo State Transitions
- Created → Active (initial state after creation)
- Active ↔ Completed (toggled by user)
- Active/Completed → Deleted (upon deletion by owning user)

## Constraints

1. **Referential Integrity**: Todo.user_id must always reference a valid User.id
2. **Access Control**: Todo operations are restricted to the owning User
3. **Data Privacy**: Users cannot access other users' Todo items
4. **Unique Email**: No duplicate email addresses allowed for User entity

## Indexes

- User.email: Unique index for fast login lookups
- Todo.user_id: Index for efficient user-scoped queries
- Todo.created_at: Index for chronological sorting