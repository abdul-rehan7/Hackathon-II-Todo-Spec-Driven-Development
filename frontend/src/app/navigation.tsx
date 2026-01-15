'use client';

import Link from 'next/link';
import { useState, useEffect } from 'react';
import { FaHome, FaPlus, FaList, FaArrowLeft, FaGithub, FaEnvelope, FaLock, FaInfoCircle, FaBook, FaCode } from 'react-icons/fa';

// Navigation component
export default function Navigation() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [hasHydrated, setHasHydrated] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    // Check authentication status after hydration
    const token = localStorage.getItem('auth-token');
    setIsAuthenticated(!!token);
    setHasHydrated(true);

    // Listen for storage changes to update auth status
    const handleStorageChange = () => {
      const token = localStorage.getItem('auth-token');
      setIsAuthenticated(!!token);
    };

    window.addEventListener('storage', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  const handleLogout = async () => {
    const token = localStorage.getItem('auth-token');
    if (token) {
      try {
        const response = await fetch('/api/auth/logout', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        // Regardless of API response, remove local token and redirect
        localStorage.removeItem('auth-token');
        window.location.href = '/';
      } catch (error) {
        // Even if API call fails, remove local token and redirect
        localStorage.removeItem('auth-token');
        window.location.href = '/';
      }
    } else {
      localStorage.removeItem('auth-token');
      window.location.href = '/';
    }
  };

  // Close mobile menu when auth state changes
  useEffect(() => {
    if (mobileMenuOpen && hasHydrated) {
      setMobileMenuOpen(false);
    }
  }, [isAuthenticated, hasHydrated]);

  // Don't show anything until hydrated to avoid flash of incorrect content
  if (!hasHydrated) {
    return (
      <nav className="bg-gray-900 text-white shadow-lg border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link href="/" className="flex-shrink-0 flex items-center">
                <span className="font-bold text-xl text-indigo-400">Donezo</span>
              </Link>
            </div>
            <div className="hidden md:flex items-center space-x-4">
              <div className="px-4 py-2 text-gray-400">...</div>
            </div>
            <div className="md:hidden flex items-center">
              <button
                className="text-gray-300 hover:text-white focus:outline-none"
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              >
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </nav>
    );
  }

  return (
    <>
      <nav className="bg-gray-900 text-white shadow-lg border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link href="/" className="flex-shrink-0 flex items-center">
                <span className="font-bold text-xl text-indigo-400">Donezo</span>
              </Link>
            </div>
            <div className="hidden md:flex items-center space-x-4">
              {!isAuthenticated ? (
                <>
                  <Link
                    href="/auth/login"
                    className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium"
                  >
                    Login
                  </Link>
                  <Link
                    href="/auth/signup"
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium"
                  >
                    Sign Up
                  </Link>
                </>
              ) : (
                <button
                  onClick={handleLogout}
                  className="px-4 py-2 bg-[var(--error)] text-white rounded-lg hover:bg-[color-mix(in_srgb,var(--error)_90%,black)] transition-colors font-medium"
                >
                  Logout
                </button>
              )}
            </div>
            <div className="md:hidden flex items-center">
              <button
                className="text-gray-300 hover:text-white focus:outline-none"
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              >
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Mobile menu backdrop */}
      {mobileMenuOpen && (
        <div
          className="fixed inset-0 z-40 bg-black bg-opacity-50"
          onClick={() => setMobileMenuOpen(false)}
        ></div>
      )}

      {/* Mobile menu drawer */}
      <div
        className={`fixed top-0 right-0 h-full w-64 bg-gray-900 shadow-lg z-50 transform transition-transform duration-300 ease-in-out ${
          mobileMenuOpen ? 'translate-x-0' : 'translate-x-full'
        }`}
      >
        <div className="flex flex-col h-full p-6">
          <div className="flex justify-end mb-8">
            <button
              className="text-gray-300 hover:text-white"
              onClick={() => setMobileMenuOpen(false)}
            >
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div className="flex-1 flex flex-col space-y-6">
            {!isAuthenticated ? (
              <>
                <Link
                  href="/auth/login"
                  className="px-4 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium text-center"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Login
                </Link>
                <Link
                  href="/auth/signup"
                  className="px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium text-center"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Sign Up
                </Link>
              </>
            ) : (
              <button
                onClick={() => {
                  handleLogout();
                  setMobileMenuOpen(false);
                }}
                className="px-4 py-3 bg-[var(--error)] text-white rounded-lg hover:bg-[color-mix(in_srgb,var(--error)_90%,black)] transition-colors font-medium"
              >
                Logout
              </button>
            )}
          </div>

          <div className="mt-auto pt-6 border-t border-gray-700">
            <p className="text-gray-400 text-sm text-center">
              &copy; {new Date().getFullYear()} Donezo. All rights reserved.
            </p>
          </div>
        </div>
      </div>
    </>
  );
}