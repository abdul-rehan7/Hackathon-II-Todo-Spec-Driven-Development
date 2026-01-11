/**
 * Utility functions for route protection and authentication checks
 */

import authService from './authService';

/**
 * Check if user is authenticated and redirect to login if not
 * @param redirectTo - Optional path to redirect to after login (defaults to current path)
 * @returns boolean indicating if user is authenticated
 */
export const requireAuth = async (redirectTo?: string): Promise<boolean> => {
  try {
    // Verify the current token is still valid
    const isValid = await authService.verifyToken();

    if (!isValid) {
      // Token is invalid, redirect to login
      const redirectPath = redirectTo || window.location.pathname;
      window.location.href = `/login?redirect=${encodeURIComponent(redirectPath)}`;
      return false;
    }

    return true;
  } catch (error) {
    console.warn('Auth verification failed:', error);
    // If verification fails, redirect to login
    const redirectPath = redirectTo || window.location.pathname;
    window.location.href = `/login?redirect=${encodeURIComponent(redirectPath)}`;
    return false;
  }
};

/**
 * Redirect to login page with optional redirect parameter
 * @param redirectPath - Path to redirect back to after login (defaults to current path)
 */
export const redirectToLogin = (redirectPath?: string): void => {
  const path = redirectPath || window.location.pathname;
  window.location.href = `/login?redirect=${encodeURIComponent(path)}`;
};

/**
 * Redirect to home page after successful authentication
 * @param redirectPath - Optional path to redirect to (defaults to home '/')
 */
export const redirectToHome = (redirectPath?: string): void => {
  const path = redirectPath || '/';
  window.location.href = path;
};

/**
 * Check if current page requires authentication
 * @param currentPage - Current page path
 * @returns boolean indicating if page requires authentication
 */
export const pageRequiresAuth = (currentPage: string): boolean => {
  // Define routes that require authentication
  const protectedRoutes = [
    '/',
    '/dashboard',
    '/todos',
    '/profile',
    // Add other protected routes as needed
  ];

  return protectedRoutes.some(route =>
    currentPage === route ||
    currentPage.startsWith(route + '/') // Match nested routes like /todos/123
  );
};

/**
 * Initialize route protection for the application
 * Should be called on app startup
 */
export const initializeRouteProtection = (): void => {
  // This could be expanded to monitor route changes
  // For now, we just export the utility functions
};