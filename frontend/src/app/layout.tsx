import './globals.css';
import { Inter } from 'next/font/google';
import Link from 'next/link';
import { FaHome, FaPlus, FaList, FaArrowLeft, FaGithub, FaEnvelope, FaLock, FaInfoCircle, FaBook, FaCode } from 'react-icons/fa';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'Todo App',
  description: 'A full-stack todo application with Next.js and FastAPI',
}

// Navigation component
function Navigation() {
  return (
    <nav className="bg-indigo-600 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex-shrink-0 flex items-center">
              <span className="font-bold text-xl">Todo App</span>
            </Link>
          </div>
          <div className="hidden md:flex items-center space-x-8">
            <Link href="/" className="flex items-center space-x-1 hover:text-indigo-200 transition-colors">
              <FaHome className="h-4 w-4" />
              <span>Home</span>
            </Link>
            <Link href="/todos" className="flex items-center space-x-1 hover:text-indigo-200 transition-colors">
              <FaList className="h-4 w-4" />
              <span>Todos</span>
            </Link>
            <Link href="/todos/add" className="flex items-center space-x-1 hover:text-indigo-200 transition-colors">
              <FaPlus className="h-4 w-4" />
              <span>Add Todo</span>
            </Link>
          </div>
          <div className="md:hidden flex items-center">
            <button className="text-white">
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
                <Link href="#" className="text-gray-300 hover:text-white transition-colors">
                  <FaInfoCircle className="inline-block mr-2 h-4 w-4" />
                  Help Center
                </Link>
              </li>
              <li>
                <Link href="#" className="text-gray-300 hover:text-white transition-colors">
                  <FaBook className="inline-block mr-2 h-4 w-4" />
                  Documentation
                </Link>
              </li>
              <li>
                <Link href="#" className="text-gray-300 hover:text-white transition-colors">
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
                <Link href="#" className="text-gray-300 hover:text-white transition-colors">
                  <FaGithub className="inline-block mr-2 h-4 w-4" />
                  GitHub
                </Link>
              </li>
              <li>
                <Link href="#" className="text-gray-300 hover:text-white transition-colors">
                  <FaEnvelope className="inline-block mr-2 h-4 w-4" />
                  Contact Us
                </Link>
              </li>
              <li>
                <Link href="#" className="text-gray-300 hover:text-white transition-colors">
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
    <html lang="en">
      <body className={`${inter.className} antialiased min-h-screen flex flex-col bg-gray-50 min-h-screen`}>
        <Navigation />
        <main className="container mx-auto px-4 py-6 max-w-7xl flex-grow">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  )
}
