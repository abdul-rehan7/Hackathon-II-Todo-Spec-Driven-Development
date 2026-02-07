# Authentication System Documentation

## Overview

The Donezo Todo application implements a secure user authentication system using JWT (JSON Web Tokens) for session management. The system supports user registration, login, logout, and protected resource access.

## Architecture

### Backend Components

- **Auth Service** (`backend/src/services/auth_service.py`): Handles user registration, authentication, and session management
- **Auth API** (`backend/src/api/auth.py`): Exposes authentication endpoints
- **Auth Middleware** (`backend/src/middleware/auth_middleware.py`): Protects API endpoints and validates tokens
- **Security Middleware** (`backend/src/middleware/security.py`): Adds security headers and input validation

### Frontend Components

- **Auth Service** (`frontend/src/services/authService.js`): Manages client-side session state
- **Todo Service** (`frontend/src/services/todoService.ts`): Includes auth headers for API calls
- **Route Guard** (`frontend/src/utils/routeGuard.js`): Redirects unauthenticated users
- **Error Handler** (`frontend/src/utils/errorHandler.js`): Handles auth-related errors

## API Endpoints

### Authentication Endpoints

#### POST `/api/auth/register`
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": "user-uuid",
    "email": "user@example.com"
  },
  "session": {
    "token": "jwt-token-string",
    "expiresAt": 1234567890
  }
}
```

#### POST `/api/auth/login`
Authenticate user and create session.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200 OK):**
```json
{
  "user": {
    "id": "user-uuid",
    "email": "user@example.com"
  },
  "session": {
    "token": "jwt-token-string",
    "expiresAt": 1234567890
  }
}
```

#### POST `/api/auth/logout`
Terminate user session.

**Response (200 OK):**
```json
{
  "message": "Successfully logged out"
}
```

#### GET `/api/auth/me`
Get current user information.

**Response (200 OK):**
```json
{
  "user": {
    "id": "user-uuid",
    "email": "user@example.com",
    "createdAt": "2024-01-01T00:00:00Z"
  }
}
```

### Protected Todo Endpoints

All todo endpoints require a valid authentication token in the `Authorization` header:

```
Authorization: Bearer <jwt-token>
```

## Security Features

### Input Validation
- Email format validation
- Password strength requirements (8+ characters, upper/lower/digits)
- Sanitization of user inputs

### Token Management
- JWT tokens with 30-minute expiration
- Secure token signing with HS256 algorithm
- Client-side token storage in localStorage

### Rate Limiting
- Built-in rate limiting capabilities (placeholder implementation)

### Security Headers
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Strict-Transport-Security: max-age=31536000; includeSubDomains
- Content-Security-Policy: default-src 'self'

## Error Handling

### HTTP Status Codes
- 200: Success
- 201: Created
- 400: Bad Request (validation errors)
- 401: Unauthorized (invalid/expired token)
- 403: Forbidden (insufficient permissions)
- 404: Not Found
- 409: Conflict (duplicate email)
- 500: Internal Server Error

### Error Responses
```json
{
  "error": "Descriptive error message"
}
```

## Implementation Details

### User Scoping
All todo operations are scoped to the authenticated user:
- Users can only create, read, update, and delete their own todos
- Unauthorized access attempts result in 404 Not Found (to avoid revealing existence of other users' data)

### Session Management
- Tokens are stored in browser localStorage
- Automatic redirect to login page on authentication failure
- Client-side token validation before API calls

## Client-Side Usage

### Checking Authentication Status
```javascript
import authService from './services/authService';

if (authService.isAuthenticated()) {
  // User is authenticated
} else {
  // Redirect to login
  window.location.href = '/login';
}
```

### Making Authenticated Requests
The todo service automatically includes auth headers for all API calls.

### Handling Logout
```javascript
await authService.logout(); // Removes token and redirects to home
```

## Security Best Practices

- Never expose authentication secrets in client-side code
- Use HTTPS in production environments
- Regularly rotate JWT secrets
- Implement proper logging for authentication events
- Monitor for suspicious authentication patterns