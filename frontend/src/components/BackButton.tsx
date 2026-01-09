'use client';

import { useRouter } from 'next/navigation';
import { FaArrowLeft } from 'react-icons/fa';
import Link from 'next/link';

interface BackButtonProps {
  href?: string;
  text?: string;
  showIcon?: boolean;
}

export default function BackButton({ href = '/', text = 'Back', showIcon = true }: BackButtonProps) {
  const router = useRouter();

  const handleClick = () => {
    if (href) {
      router.push(href);
    } else {
      router.back();
    }
  };

  return (
    <div className="mb-6">
      <button
        onClick={handleClick}
        className="flex items-center text-indigo-600 hover:text-indigo-800 transition-colors"
      >
        {showIcon && <FaArrowLeft className="mr-2" />}
        {text !== '←' && <span>{text}</span>}
      </button>
    </div>
  );
}