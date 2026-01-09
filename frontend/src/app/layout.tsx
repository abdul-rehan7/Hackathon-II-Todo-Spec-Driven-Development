import './globals.css';
import { Inter } from 'next/font/google';
import Link from 'next/link';
import { FaHome, FaPlus, FaList, FaArrowLeft } from 'react-icons/fa';

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

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} antialiased min-h-screen bg-gray-50`}>
        <Navigation />
        <main className="container mx-auto px-4 py-6 max-w-7xl">
          {children}
        </main>
      </body>
    </html>
  )
}
