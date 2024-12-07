'use client';

import { useEffect, useState } from 'react';
import { GoogleMap, LoadScript, Marker } from '@react-google-maps/api';
import BackButton from '@/components/BackButton';
import Logo from '@/components/Logo';

interface Vehicle {
  id: number;
  make: string;
  model: string;
  year: number;
  license_plate: string;
  status: string;
  mileage: number;
  location_lat: number;
  location_lng: number;
}

const containerStyle = {
  width: '100%',
  height: '400px'
};

const center = {
  lat: -33.865143,
  lng: 151.209900
};

export default function MyFleet() {
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchVehicles();
  }, []);

  const fetchVehicles = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/vehicles/');
      if (!response.ok) {
        throw new Error('Failed to fetch vehicles');
      }
      const data = await response.json();
      setVehicles(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching vehicles:', error);
      setError('Failed to load vehicles. Please try again later.');
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
          <strong className="font-bold">Error!</strong>
          <span className="block sm:inline"> {error}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <Logo />
        <BackButton />
      </div>
      <h1 className="text-3xl font-bold mb-6 text-gray-800 dark:text-white">My Fleet</h1>

      {/* Fleet Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-2 text-gray-800 dark:text-white">Total Vehicles</h2>
          <p className="text-3xl font-bold text-blue-600">{vehicles.length}</p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-2 text-gray-800 dark:text-white">Active Vehicles</h2>
          <p className="text-3xl font-bold text-green-600">
            {vehicles.filter(v => v.status === 'active').length}
          </p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-2 text-gray-800 dark:text-white">In Maintenance</h2>
          <p className="text-3xl font-bold text-yellow-600">
            {vehicles.filter(v => v.status === 'maintenance').length}
          </p>
        </div>
      </div>

      {/* Map View */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-white">Vehicle Locations</h2>
        <LoadScript googleMapsApiKey="YOUR_GOOGLE_MAPS_API_KEY">
          <GoogleMap
            mapContainerStyle={containerStyle}
            center={center}
            zoom={10}
          >
            {vehicles.map((vehicle) => (
              <Marker
                key={vehicle.id}
                position={{ lat: Number(vehicle.location_lat), lng: Number(vehicle.location_lng) }}
                title={`${vehicle.year} ${vehicle.make} ${vehicle.model}`}
              />
            ))}
          </GoogleMap>
        </LoadScript>
      </div>

      {/* Vehicle List */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
        <h2 className="text-xl font-semibold p-6 border-b border-gray-200 dark:border-gray-700 text-gray-800 dark:text-white">
          Vehicle List
        </h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead className="bg-gray-50 dark:bg-gray-900">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Vehicle
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  License Plate
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Mileage
                </th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              {vehicles.map((vehicle) => (
                <tr key={vehicle.id}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900 dark:text-white">
                      {vehicle.year} {vehicle.make} {vehicle.model}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-500 dark:text-gray-300">{vehicle.license_plate}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                      vehicle.status === 'active'
                        ? 'bg-green-100 text-green-800'
                        : vehicle.status === 'maintenance'
                        ? 'bg-yellow-100 text-yellow-800'
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {vehicle.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                    {vehicle.mileage.toLocaleString()} km
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
