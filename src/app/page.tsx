import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white dark:from-gray-900 dark:to-gray-800">
      <main className="container mx-auto px-4 py-16">
        <h1 className="text-4xl font-bold text-center mb-4 text-gray-800 dark:text-white">
          Welcome to eyeFleet
        </h1>
        <p className="text-center mb-12 text-gray-600 dark:text-gray-300">
          Manage your fleet with ease and efficiency
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* My Fleet Card */}
          <Link href="/my-fleet" className="transform hover:scale-105 transition-transform duration-200">
            <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg hover:shadow-xl">
              <h2 className="text-xl font-semibold mb-2 text-gray-800 dark:text-white">My Fleet</h2>
              <p className="text-gray-600 dark:text-gray-300">View and manage your entire fleet in one place</p>
            </div>
          </Link>

          {/* Todo Card */}
          <Link href="/todo" className="transform hover:scale-105 transition-transform duration-200">
            <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg hover:shadow-xl">
              <h2 className="text-xl font-semibold mb-2 text-gray-800 dark:text-white">Todo</h2>
              <p className="text-gray-600 dark:text-gray-300">Track and manage maintenance tasks</p>
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
      </main>
    </div>
  );
}
