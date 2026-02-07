/**
 * Authentication service for handling session management on the frontend
 */
// Use relative URLs to go through Next.js proxy
const API_BASE_URL = '/api/auth';  // Next.js proxy routes

class AuthService {
  /**
   * Check if user is currently authenticated
   */
  isAuthenticated() {
    const token = this.getToken();
    return !!token;
  }

  /**
   * Get the authentication token from localStorage
   */
  getToken() {
    return localStorage.getItem('auth-token');
  }

  /**
   * Set the authentication token in localStorage
   */
  setToken(token) {
    const oldValue = localStorage.getItem('auth-token');
    localStorage.setItem('auth-token', token);

    // Dispatch a storage event to notify other parts of the app
    window.dispatchEvent(new StorageEvent('storage', {
      key: 'auth-token',
      oldValue: oldValue,
      newValue: token,
      url: window.location.href,
      storageArea: localStorage
    }));
  }

  /**
   * Remove the authentication token from localStorage
   */
  removeToken() {
    const oldValue = localStorage.getItem('auth-token');
    localStorage.removeItem('auth-token');

    // Dispatch a storage event to notify other parts of the app
    window.dispatchEvent(new StorageEvent('storage', {
      key: 'auth-token',
      oldValue: oldValue,
      newValue: null,
      url: window.location.href,
      storageArea: localStorage
    }));
  }

  /**
   * Get user information from the API
   */
  async getCurrentUser() {
    const token = this.getToken();

    if (!token) {
      throw new Error('No authentication token found');
    }

    try {
      const response = await fetch(`${API_BASE_URL}/me`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        if (response.status === 401) {
          // Token is invalid or expired, remove it
          this.removeToken();
          throw new Error('Authentication token is invalid or expired');
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data.user;
    } catch (error) {
      console.error('Error fetching user data:', error);
      throw error;
    }
  }

  /**
   * Login user with email and password
   */
  async login(email, password) {
    try {
      const formData = new FormData();
      formData.append('email', email);
      formData.append('password', password);

      const response = await fetch(`${API_BASE_URL}/login`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Login failed');
      }

      if (data.session && data.session.token) {
        this.setToken(data.session.token);
        return data.user;
      } else {
        throw new Error('Invalid response format from server');
      }
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }

  /**
   * Register a new user
   */
  async register(email, password) {
    try {
      const formData = new FormData();
      formData.append('email', email);
      formData.append('password', password);

      const response = await fetch(`${API_BASE_URL}/register`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Registration failed');
      }

      if (data.session && data.session.token) {
        this.setToken(data.session.token);
        return data.user;
      } else {
        throw new Error('Invalid response format from server');
      }
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  }

  /**
   * Logout the current user
   */
  async logout() {
    try {
      const token = this.getToken();

      if (token) {
        // Call the logout API endpoint
        const response = await fetch(`${API_BASE_URL}/logout`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        // Even if the API call fails, we should still remove the local token
        // to prevent further unauthorized requests
        if (!response.ok) {
          console.warn('Logout API call failed, but removing local token');
        }
      }

      // Remove the token from localStorage
      this.removeToken();

      // Redirect to home page after logout
      window.location.href = '/';
    } catch (error) {
      console.error('Logout error:', error);
      // Still remove the token even if the API call fails
      this.removeToken();
      window.location.href = '/';
    }
  }

  /**
   * Verify if the current token is still valid
   */
  async verifyToken() {
    try {
      await this.getCurrentUser();
      return true;
    } catch (error) {
      return false;
    }
  }
}

// Create a singleton instance
const authService = new AuthService();
export default authService;