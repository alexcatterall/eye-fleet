'use client';

import Link from 'next/link';

export default function BackButton() {
  return (
    <Link
      href="/"
      className="absolute top-4 left-4 px-4 py-2 bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-white rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors font-mono text-sm flex items-center shadow-sm"
    >
      ← Home
    </Link>
  );
}
