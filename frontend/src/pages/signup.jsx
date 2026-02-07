import { useRouter } from 'next/router';
import { useEffect } from 'react';

const SignupPage = () => {
  const router = useRouter();

  useEffect(() => {
    // Redirect to the new app router signup page
    router.push('/auth/signup');
  }, [router]);

  return null;
};

export default SignupPage;