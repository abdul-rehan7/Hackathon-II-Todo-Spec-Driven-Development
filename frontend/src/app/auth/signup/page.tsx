'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import SignupForm from '../../../components/auth/SignupForm';

const SignupPage = () => {
  const router = useRouter();
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('auth-token');
    if (token) {
      // TODO: Verify token validity
      setIsLoggedIn(true);
    }
  }, []);

  useEffect(() => {
    if (isLoggedIn) {
      // Redirect to dashboard if already logged in
      router.push('/todos');
    }
  }, [isLoggedIn, router]);

  const handleSignup = (userData) => {
    console.log('Signup successful:', userData);
    // Redirect to dashboard after successful signup
    router.push('/todos');
  };

  if (isLoggedIn) {
    return <div className="min-h-screen flex items-center justify-center bg-[var(--background)]">
      <div className="text-lg text-[var(--text-primary)]">Redirecting...</div>
    </div>;
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-[var(--background)] py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center animate-fade-in">
          <h2 className="mt-6 text-center text-3xl font-bold text-[var(--text-primary)]">
            Create your account
          </h2>
          <p className="mt-2 text-center text-sm text-[var(--text-secondary)]">
            Join Donezo to manage your tasks
          </p>
        </div>
        <div className="mt-8 bg-[var(--card-bg)] rounded-2xl shadow-xl p-8 border border-[var(--card-border)] transform transition-all duration-300 hover:shadow-2xl hover:-translate-y-1">
          <SignupForm onSignup={handleSignup} />

          <div className="mt-6 text-center">
            <p className="text-sm text-[var(--text-secondary)]">
              Already have an account?{' '}
              <a
                href="/auth/login"
                className="font-medium text-[var(--primary)] hover:text-[var(--primary-hover)] transition-colors duration-200"
              >
                Sign in
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SignupPage;