'use client';

import BackButton from '@/components/BackButton';
import Logo from '@/components/Logo';

export default function Todo() {
  return (
    <div className="container mx-auto px-4 py-8">
      <BackButton />
      <Logo />
      <h1 className="text-3xl font-bold mb-6 text-gray-800 dark:text-white">To-do List</h1>
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        <p className="text-gray-600 dark:text-gray-300">Todo list will be displayed here.</p>
      </div>
    </div>
  );
}
