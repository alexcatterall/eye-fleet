'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import BackButton from '@/components/BackButton';
import Logo from '@/components/Logo';

interface Vehicle {
  id: number;
  registration_number: string;
  manufacturer: string;
  model: string;
  type: string;
  driver: string;
  status: string;
  location: string;
  fuel_level: number;
  on_trip: boolean;
  mileage: string;
}

export default function EditAsset() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const registration = searchParams.get('id');
  
  const [formData, setFormData] = useState<Vehicle>({
    id: 0,
    registration_number: '',
    manufacturer: '',
    model: '',
    type: '',
    driver: '',
    status: '',
    location: '',
    fuel_level: 0,
    on_trip: false,
    mileage: '',
  });

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchAssetDetails = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/maintenance/assets/?registration_number=${encodeURIComponent(registration)}`);
        if (!response.ok) {
          throw new Error('Failed to fetch asset details');
        }
        const data = await response.json();
        if (data && data.length > 0) {
          setFormData(data[0]); // Take the first matching asset
        } else {
          throw new Error('Asset not found');
        }
        setLoading(false);
      } catch (error) {
        console.error('Error fetching asset details:', error);
        setError('Failed to load asset details. Please try again later.');
        setLoading(false);
      }
    };

    if (registration) {
      fetchAssetDetails();
    }
  }, [registration]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://localhost:8000/api/maintenance/assets/${formData.id}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`Error: ${errorData.detail || response.statusText}`);
      }

      alert('Asset updated successfully!');
      router.push('/my-fleet');
    } catch (error) {
      console.error('Error updating asset:', error);
      alert(`Failed to update asset: ${error.message}`);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this asset? This action cannot be undone.')) {
      try {
        // First, get the asset details to ensure it exists
        const getResponse = await fetch(`http://localhost:8000/api/maintenance/assets/?registration_number=${encodeURIComponent(registration)}`);
        if (!getResponse.ok) {
          throw new Error('Failed to find asset');
        }
        const assets = await getResponse.json();
        if (!assets || assets.length === 0) {
          throw new Error('Asset not found');
        }

        const assetId = assets[0].id;
        
        // Delete the asset using the ID endpoint
        const deleteResponse = await fetch(`http://localhost:8000/api/maintenance/assets/${assetId}/`, {
          method: 'DELETE',
        });
        
        if (!deleteResponse.ok) {
          const errorData = await deleteResponse.json();
          throw new Error(`Error: ${errorData.detail || deleteResponse.statusText}`);
        }

        alert('Asset deleted successfully!');
        router.push('/my-fleet');
      } catch (error) {
        console.error('Error deleting asset:', error);
        alert(`Failed to delete asset: ${error.message}`);
      }
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
      <h1 className="text-3xl font-bold mb-6 text-gray-800 dark:text-white">Edit Asset</h1>

      <form onSubmit={handleSubmit} className="max-w-2xl mx-auto">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Registration Number */}
            <div>
              <label htmlFor="registration_number" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Registration Number
              </label>
              <input
                type="text"
                id="registration_number"
                name="registration_number"
                value={formData.registration_number}
                onChange={handleChange}
                disabled
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white bg-gray-100"
              />
            </div>

            {/* Manufacturer */}
            <div>
              <label htmlFor="manufacturer" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Manufacturer
              </label>
              <input
                type="text"
                id="manufacturer"
                name="manufacturer"
                value={formData.manufacturer}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              />
            </div>

            {/* Model */}
            <div>
              <label htmlFor="model" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Model
              </label>
              <input
                type="text"
                id="model"
                name="model"
                value={formData.model}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              />
            </div>

            {/* Type */}
            <div>
              <label htmlFor="type" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Type
              </label>
              <select
                id="type"
                name="type"
                value={formData.type}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              >
                <option value="">Select type</option>
                <option value="car">Car</option>
                <option value="truck">Truck</option>
                <option value="van">Van</option>
              </select>
            </div>

            {/* Driver */}
            <div>
              <label htmlFor="driver" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Driver
              </label>
              <input
                type="text"
                id="driver"
                name="driver"
                value={formData.driver}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              />
            </div>

            {/* Status */}
            <div>
              <label htmlFor="status" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Status
              </label>
              <select
                id="status"
                name="status"
                value={formData.status}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              >
                <option value="">Select status</option>
                <option value="active">Active</option>
                <option value="maintenance">Maintenance</option>
                <option value="inactive">Inactive</option>
              </select>
            </div>

            {/* Location */}
            <div>
              <label htmlFor="location" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Location
              </label>
              <input
                type="text"
                id="location"
                name="location"
                value={formData.location}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              />
            </div>

            {/* Fuel Level */}
            <div>
              <label htmlFor="fuel_level" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Fuel Level (%)
              </label>
              <input
                type="number"
                id="fuel_level"
                name="fuel_level"
                value={formData.fuel_level}
                onChange={handleChange}
                min="0"
                max="100"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              />
            </div>

            {/* Mileage */}
            <div>
              <label htmlFor="mileage" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Mileage (km)
              </label>
              <input
                type="number"
                id="mileage"
                name="mileage"
                value={formData.mileage}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              />
            </div>

            {/* On Trip */}
            <div className="col-span-2">
              <label className="flex items-center space-x-3">
                <input
                  type="checkbox"
                  id="on_trip"
                  name="on_trip"
                  checked={formData.on_trip}
                  onChange={handleChange}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Currently On Trip</span>
              </label>
            </div>
          </div>

          <div className="flex justify-between space-x-4">
            <button
              type="button"
              onClick={handleDelete}
              className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
            >
              Delete Asset
            </button>
            <div className="flex space-x-4">
              <button
                type="button"
                onClick={() => router.push('/my-fleet')}
                className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Save Changes
              </button>
            </div>
          </div>
        </div>
      </form>
    </div>
  );
}
