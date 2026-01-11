import { useRouter } from 'next/router';
import authService from '../../services/authService';

const LogoutButton = () => {
  const router = useRouter();

  const handleLogout = async () => {
    try {
      // Call the auth service to handle logout
      await authService.logout();

      // Redirect to login page after logout
      router.push('/login');
    } catch (error) {
      console.error('Logout error:', error);
      // Even if API call fails, redirect to login
      router.push('/login');
    }
  };

  return (
    <button
      onClick={handleLogout}
      className="px-4 py-2 bg-[var(--error)] text-white rounded-lg hover:bg-[color-mix(in_srgb,var(--error)_90%,black)] transition-colors font-medium"
    >
      Logout
    </button>
  );
};

export default LogoutButton;