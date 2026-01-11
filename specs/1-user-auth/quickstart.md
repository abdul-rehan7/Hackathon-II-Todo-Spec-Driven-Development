# Quickstart Guide: User Authentication

**Feature**: User Authentication with better-auth.com
**Date**: 2026-01-10
**Branch**: 1-user-auth

## Overview

This guide provides step-by-step instructions for implementing user authentication in the Donezo Todo application using better-auth.com. The implementation includes user registration, login, logout, and protected Todo operations.

## Prerequisites

- Node.js and npm installed
- Better-auth.com account and credentials
- Environment variables configured for auth secrets
- Database configured with User and Todo tables

## Setup Steps

### 1. Install Dependencies

```bash
npm install better-auth @better-auth/react
```

### 2. Configure Environment Variables

Create or update your `.env` file:

```env
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-secret-key-here
BETTER_AUTH_EMAIL_FROM=your-app@example.com
```

### 3. Initialize Better Auth

Create `lib/auth.js`:

```javascript
import { init } from "better-auth";
import { betterAuthClient } from "@better-auth/client";

export const auth = init({
  secret: process.env.BETTER_AUTH_SECRET,
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL,
  emailAndPassword: {
    enabled: true,
  },
});

export const client = betterAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL,
});
```

### 4. Create Auth Components

Create `components/auth/LoginForm.jsx`:

```jsx
import { useState } from 'react';
import { signIn } from 'lib/auth';

const LoginForm = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const result = await signIn('credentials', {
        email,
        password,
        redirect: false
      });

      if (result?.error) {
        setError(result.error);
      } else {
        onLogin();
      }
    } catch (err) {
      setError('Login failed. Please try again.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
        />
      </div>
      <div>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
      </div>
      {error && <div className="error">{error}</div>}
      <button type="submit">Login</button>
    </form>
  );
};

export default LoginForm;
```

### 5. Create Protected Route Component

Create `components/auth/ProtectedRoute.jsx`:

```jsx
import { useEffect } from 'react';
import { useSession } from '@better-auth/react';
import { useRouter } from 'next/router';

const ProtectedRoute = ({ children }) => {
  const { session, isLoading } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !session) {
      router.push('/login');
    }
  }, [session, isLoading, router]);

  if (isLoading || !session) {
    return <div>Loading...</div>;
  }

  return children;
};

export default ProtectedRoute;
```

### 6. Update Todo API Calls

Modify your Todo service to include authentication headers:

```javascript
// services/todoService.js
const apiCall = async (endpoint, options = {}) => {
  const token = localStorage.getItem('auth-token'); // or however you store the token

  const response = await fetch(`/api${endpoint}`, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (response.status === 401) {
    // Redirect to login if unauthorized
    window.location.href = '/login';
    return null;
  }

  return response.json();
};
```

### 7. Protect Backend Routes

In your backend API routes, add authentication middleware:

```javascript
// middleware/auth_middleware.py (if using Python backend)
def require_auth(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {'error': 'Authentication required'}, 401

        # Verify token and get user
        user = verify_token(token.replace('Bearer ', ''))
        if not user:
            return {'error': 'Invalid token'}, 401

        return func(user=user, *args, **kwargs)
    return wrapper
```

## Testing the Implementation

### Frontend Tests

1. Verify registration form creates new users
2. Verify login form authenticates existing users
3. Verify protected routes redirect unauthenticated users
4. Verify logout functionality

### Backend Tests

1. Verify authentication middleware protects routes
2. Verify user-scoped Todo access
3. Verify unauthorized access attempts are rejected
4. Verify user data isolation

## Common Issues and Solutions

1. **Environment variables not loading**: Ensure .env file is in the correct location and restart development server
2. **Cross-origin issues**: Configure CORS appropriately for auth endpoints
3. **Session not persisting**: Check browser storage settings and auth configuration
4. **Token expiration**: Implement token refresh mechanisms as needed

## Next Steps

1. Add password reset functionality
2. Implement multi-factor authentication
3. Add user profile management
4. Set up audit logging for security events