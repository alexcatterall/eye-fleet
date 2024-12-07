'use client';

import { useState, useEffect } from 'react';
import { GoogleMap, LoadScript, Marker } from '@react-google-maps/api';

// Mock data for demonstration
const mockVehicles = [
  {
    id: 1,
    make: 'Toyota',
    model: 'Camry',
    status: 'active',
    location: { lat: -33.865143, lng: 151.209900 }
  },
  {
    id: 2,
    make: 'Ford',
    model: 'Ranger',
    status: 'maintenance',
    location: { lat: -33.863000, lng: 151.211000 }
  },
  // Add more mock vehicles as needed
];

const mapContainerStyle = {
  width: '100%',
  height: '500px'
};

const center = {
  lat: -33.865143,
  lng: 151.209900
};

export default function MyFleet() {
  const [vehicles, setVehicles] = useState(mockVehicles);
  
  const stats = {
    total: vehicles.length,
    active: vehicles.filter(v => v.status === 'active').length,
    maintenance: vehicles.filter(v => v.status === 'maintenance').length,
    retired: vehicles.filter(v => v.status === 'retired').length
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6 text-gray-800 dark:text-white">My Fleet</h1>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-600 dark:text-gray-300">Total Vehicles</h3>
          <p className="text-3xl font-bold text-blue-600 dark:text-blue-400">{stats.total}</p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-600 dark:text-gray-300">Active</h3>
          <p className="text-3xl font-bold text-green-600 dark:text-green-400">{stats.active}</p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-600 dark:text-gray-300">In Maintenance</h3>
          <p className="text-3xl font-bold text-yellow-600 dark:text-yellow-400">{stats.maintenance}</p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-600 dark:text-gray-300">Retired</h3>
          <p className="text-3xl font-bold text-gray-600 dark:text-gray-400">{stats.retired}</p>
        </div>
      </div>

      {/* Fleet List */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-8">
        <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-white">Fleet Overview</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full table-auto">
            <thead>
              <tr className="bg-gray-50 dark:bg-gray-700">
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Vehicle</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Location</th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              {vehicles.map((vehicle) => (
                <tr key={vehicle.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-gray-700 dark:text-gray-300">
                    {vehicle.make} {vehicle.model}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                      ${vehicle.status === 'active' ? 'bg-green-100 text-green-800' : 
                        vehicle.status === 'maintenance' ? 'bg-yellow-100 text-yellow-800' : 
                        'bg-gray-100 text-gray-800'}`}>
                      {vehicle.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-gray-700 dark:text-gray-300">
                    {`${vehicle.location.lat.toFixed(6)}, ${vehicle.location.lng.toFixed(6)}`}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Map Section */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-white">Fleet Location</h2>
        <LoadScript googleMapsApiKey="YOUR_GOOGLE_MAPS_API_KEY">
          <GoogleMap
            mapContainerStyle={mapContainerStyle}
            center={center}
            zoom={13}
          >
            {vehicles.map((vehicle) => (
              <Marker
                key={vehicle.id}
                position={vehicle.location}
                title={`${vehicle.make} ${vehicle.model}`}
              />
            ))}
          </GoogleMap>
        </LoadScript>
      </div>
    </div>
  );
}
