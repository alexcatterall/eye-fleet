import Image from 'next/image';
import Link from 'next/link';
import Logo from '@/components/Logo';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24 relative">
      <div className="absolute top-8 left-8">
        <Logo />
      </div>
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold mb-8 text-center text-gray-800 dark:text-white">
          Welcome to Eye Fleet!
        </h1>
        <div className="flex justify-center mb-8">
        </div>
        <div className="flex items-center justify-center gap-4 mb-8">
          <p className="text-sm font-mono text-gray-600 dark:text-gray-400">
            Built @
          </p>
          <Image
            src="/ef_hack.avif"
            alt="Eye Fleet"
            width={200}
            height={150}
            className="rounded-lg shadow-lg"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-12">
          {/* My Fleet Card */}
          <Link href="/my-fleet" className="transform hover:scale-105 transition-transform duration-200">
            <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg hover:shadow-xl">
              <h2 className="text-xl font-semibold mb-2 text-gray-800 dark:text-white">My Fleet</h2>
              <p className="text-gray-600 dark:text-gray-300">View and manage your entire fleet in one place</p>
            </div>
          </Link>

          {/* Fleet Vision Card */}
          <Link href="/fleet-vision" className="transform hover:scale-105 transition-transform duration-200">
            <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg hover:shadow-xl">
              <h2 className="text-xl font-semibold mb-2 text-gray-800 dark:text-white">Fleet Vision</h2>
              <p className="text-gray-600 dark:text-gray-300">Interactive map view with real-time chat functionality</p>
            </div>
          </Link>

          {/* Vehicle Card */}
          <Link href="/vehicle" className="transform hover:scale-105 transition-transform duration-200">
            <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg hover:shadow-xl">
              <h2 className="text-xl font-semibold mb-2 text-gray-800 dark:text-white">Vehicle</h2>
              <p className="text-gray-600 dark:text-gray-300">View detailed vehicle information</p>
            </div>
          </Link>

          {/* Add Vehicle Card */}
          <Link href="/add-vehicle" className="transform hover:scale-105 transition-transform duration-200">
            <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg hover:shadow-xl">
              <h2 className="text-xl font-semibold mb-2 text-gray-800 dark:text-white">Add Vehicle</h2>
              <p className="text-gray-600 dark:text-gray-300">Add a new vehicle to your fleet</p>
            </div>
          </Link>
        </div>
      </div>
    </main>
  );
}
