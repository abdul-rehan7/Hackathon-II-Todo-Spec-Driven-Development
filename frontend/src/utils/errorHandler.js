/**
 * Comprehensive error handling utilities for authentication and API failures
 */

/**
 * Handle authentication-related errors
 * @param error - The error object
 * @param context - Context where the error occurred (e.g., 'fetch', 'mutation', 'auth')
 * @returns formatted error object
 */
export const handleAuthError = (error: any, context: string = 'general'): { type: string; message: string; shouldRedirect: boolean } => {
  // Check if it's a network error
  if (!error.response) {
    return {
      type: 'network',
      message: 'Network error - please check your connection',
      shouldRedirect: false
    };
  }

  // Check for authentication errors
  if (error.response?.status === 401) {
    return {
      type: 'authentication',
      message: 'Session expired. Please log in again.',
      shouldRedirect: true
    };
  }

  // Check for authorization errors
  if (error.response?.status === 403) {
    return {
      type: 'authorization',
      message: 'Access denied. You do not have permission to perform this action.',
      shouldRedirect: true
    };
  }

  // Default error handling
  return {
    type: 'general',
    message: error.response?.data?.detail || error.message || 'An unexpected error occurred',
    shouldRedirect: false
  };
};

/**
 * Handle API errors with different strategies based on error type
 * @param error - The error object
 * @param options - Configuration options for error handling
 */
export const handleApiError = (error: any, options: {
  showAlert?: boolean;
  redirectToLogin?: boolean;
  customMessage?: string;
} = {}) => {
  const { showAlert = true, redirectToLogin = false, customMessage = null } = options;

  // Extract error information
  const errorInfo = handleAuthError(error);

  // Log the error for debugging
  console.error(`API Error (${errorInfo.type}):`, error);

  // Show alert if requested
  if (showAlert) {
    const message = customMessage || errorInfo.message;
    alert(message);
  }

  // Handle redirect if needed
  if (errorInfo.shouldRedirect || redirectToLogin) {
    window.location.href = '/login';
  }

  // Return error info for further processing
  return errorInfo;
};

/**
 * Generic error boundary helper for React components
 */
export class ErrorHandler {
  static captureError(error: Error, info: any) {
    console.error('Error caught by boundary:', error, info);

    // In a real application, you might want to log to an error tracking service
    // Example: Sentry.captureException(error);
  }

  static getErrorMessage(error: any): string {
    if (error instanceof TypeError && error.message.includes('NetworkError')) {
      return 'Network error - please check your connection';
    }

    if (error.response) {
      // Server responded with error status
      const status = error.response.status;

      switch (status) {
        case 400:
          return error.response.data?.detail || 'Bad request - please check your input';
        case 401:
          return 'Authentication required - please log in';
        case 403:
          return 'Access forbidden - insufficient permissions';
        case 404:
          return 'Resource not found';
        case 500:
          return 'Server error - please try again later';
        default:
          return `Request failed with status ${status}`;
      }
    }

    return error.message || 'An unknown error occurred';
  }
}

/**
 * Retry mechanism for failed requests
 */
export const retryRequest = async (
  requestFn: () => Promise<any>,
  retries: number = 3,
  delay: number = 1000
): Promise<any> => {
  for (let i = 0; i < retries; i++) {
    try {
      return await requestFn();
    } catch (error) {
      if (i === retries - 1) {
        // Last attempt, throw the error
        throw error;
      }

      // Check if it's an authentication error - don't retry those
      if (error.response?.status === 401) {
        throw error;
      }

      // Wait before retrying
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
};