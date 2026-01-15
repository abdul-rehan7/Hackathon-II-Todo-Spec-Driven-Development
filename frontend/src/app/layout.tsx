'use client';

import './globals.css';
import { Inter } from 'next/font/google';
import Link from 'next/link';
import { useState, useEffect } from 'react';
import { FaHome, FaPlus, FaList, FaArrowLeft, FaGithub, FaEnvelope, FaLock, FaInfoCircle, FaBook, FaCode } from 'react-icons/fa';

const inter = Inter({ subsets: ['latin'] });


// Navigation component
function Navigation() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check authentication status on mount
    const token = localStorage.getItem('auth-token');
    setIsAuthenticated(!!token);
    setLoading(false);

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

  if (loading) {
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
              <div className="px-4 py-2 text-gray-400">Loading...</div>
            </div>
            <div className="md:hidden flex items-center">
              <button className="text-gray-300 hover:text-white">
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
            <button className="text-gray-300 hover:text-white">
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

// Footer component
function Footer() {
  return (
    <footer className="bg-gray-800 text-white py-8 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-4">Todo App</h3>
            <p className="text-gray-300 text-sm">
              A full-stack todo application designed to help you manage your tasks efficiently and effectively.
            </p>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/" className="text-gray-300 hover:text-white transition-colors">
                  <FaHome className="inline-block mr-2 h-4 w-4" />
                  Home
                </Link>
              </li>
              <li>
                <Link href="/todos" className="text-gray-300 hover:text-white transition-colors">
                  <FaList className="inline-block mr-2 h-4 w-4" />
                  Todos
                </Link>
              </li>
              <li>
                <Link href="/todos/add" className="text-gray-300 hover:text-white transition-colors">
                  <FaPlus className="inline-block mr-2 h-4 w-4" />
                  Add Todo
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">Resources</h3>
            <ul className="space-y-2">
              <li>
                <Link href="#" target="_blank" className="text-gray-300 hover:text-white transition-colors">
                  <FaInfoCircle className="inline-block mr-2 h-4 w-4" />
                  Help Center
                </Link>
              </li>
              <li>
                <Link href="#" target="_blank" className="text-gray-300 hover:text-white transition-colors">
                  <FaBook className="inline-block mr-2 h-4 w-4" />
                  Documentation
                </Link>
              </li>
              <li>
                <Link href="#" target="_blank" className="text-gray-300 hover:text-white transition-colors">
                  <FaCode className="inline-block mr-2 h-4 w-4" />
                  API Reference
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">Connect</h3>
            <ul className="space-y-2">
              <li>
                <Link href="https://github.com/abdul-rehan7" target="_blank" className="text-gray-300 hover:text-white transition-colors">
                  <FaGithub className="inline-block mr-2 h-4 w-4" />
                  GitHub
                </Link>
              </li>
              <li>
                <Link href="mailto:abdulrehan0317@gmail.com" target="_blank" className="text-gray-300 hover:text-white transition-colors">
                  <FaEnvelope className="inline-block mr-2 h-4 w-4" />
                  Contact Us
                </Link>
              </li>
              <li>
                <Link href="#" target="_blank" className="text-gray-300 hover:text-white transition-colors">
                  <FaLock className="inline-block mr-2 h-4 w-4" />
                  Privacy Policy
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-700 mt-8 pt-6 text-center">
          <p className="text-gray-400 text-sm">
            © {new Date().getFullYear()} Todo App. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} antialiased min-h-screen flex flex-col bg-base text-base`}>
        <Navigation />
        <main className="container mx-auto px-4 py-6 max-w-7xl flex-grow">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  )
}
