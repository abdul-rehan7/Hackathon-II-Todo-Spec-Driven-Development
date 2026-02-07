import './globals.css';
import { Inter } from 'next/font/google';
import Link from 'next/link';
import Navigation from './navigation';
import { FaHome, FaPlus, FaList, FaArrowLeft, FaGithub, FaEnvelope, FaLock, FaInfoCircle, FaBook, FaCode } from 'react-icons/fa';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'Donezo',
  description: 'A full-stack todo application with Next.js and FastAPI',
};

// Footer component
function Footer() {
  return (
    <footer className="bg-gray-800 text-white py-8 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-4">Donezo</h3>
            <p className="text-gray-300 text-sm">
              A full-stack todo application designed to help you manage your tasks efficiently and effectively.
            </p>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">Resources</h3>
            <ul className="space-y-2">
              <li>
                <a href="#" target="_blank" className="text-gray-300 hover:text-white transition-colors">
                  <FaInfoCircle className="inline-block mr-2 h-4 w-4" />
                  Help Center
                </a>
              </li>
              <li>
                <a href="#" target="_blank" className="text-gray-300 hover:text-white transition-colors">
                  <FaBook className="inline-block mr-2 h-4 w-4" />
                  Documentation
                </a>
              </li>
              <li>
                <a href="#" target="_blank" className="text-gray-300 hover:text-white transition-colors">
                  <FaCode className="inline-block mr-2 h-4 w-4" />
                  API Reference
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">Connect</h3>
            <ul className="space-y-2">
              <li>
                <a href="https://github.com/abdul-rehan7" target="_blank" className="text-gray-300 hover:text-white transition-colors">
                  <FaGithub className="inline-block mr-2 h-4 w-4" />
                  GitHub
                </a>
              </li>
              <li>
                <a href="mailto:abdulrehan0317@gmail.com" target="_blank" className="text-gray-300 hover:text-white transition-colors">
                  <FaEnvelope className="inline-block mr-2 h-4 w-4" />
                  Contact Us
                </a>
              </li>
              <li>
                <a href="#" target="_blank" className="text-gray-300 hover:text-white transition-colors">
                  <FaLock className="inline-block mr-2 h-4 w-4" />
                  Privacy Policy
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-700 mt-8 pt-6 text-center">
          <p className="text-gray-400 text-sm">
            © {new Date().getFullYear()} Donezo. All rights reserved.
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
