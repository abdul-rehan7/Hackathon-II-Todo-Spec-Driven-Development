import { useRouter } from 'next/router';
import { useEffect } from 'react';

const LoginPage = () => {
  const router = useRouter();

  useEffect(() => {
    // Redirect to the new app router login page
    router.push('/auth/login');
  }, [router]);

  return null;
};

export default LoginPage;