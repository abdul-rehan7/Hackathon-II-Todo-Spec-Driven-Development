import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import authService from '../../services/authService';

const ProtectedRoute = ({ children }) => {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const authStatus = await authService.verifyToken();
        setIsAuthenticated(authStatus);

        if (!authStatus) {
          // Redirect to login if not authenticated
          router.push('/login');
        }
      } catch (error) {
        console.error('Auth verification error:', error);
        setIsAuthenticated(false);
        router.push('/login');
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, [router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[var(--background)]">
        <div className="text-lg text-[var(--text-primary)]">Loading...</div>
      </div>
    );
  }

  if (isAuthenticated === false) {
    // Don't render children if not authenticated (redirect happens above)
    return null;
  }

  return children;
};

export default ProtectedRoute;