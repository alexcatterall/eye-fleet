'use client';

import { useState } from 'react';

export default function AddVehicle() {
  const [formData, setFormData] = useState({
    make: '',
    model: '',
    year: '',
    licensePlate: '',
    vin: '',
    mileage: '',
    fuelType: 'gasoline',
    status: 'active',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Implement API call to save vehicle
    console.log('Vehicle data:', formData);
    alert('Vehicle added successfully!');
    // Reset form
    setFormData({
      make: '',
      model: '',
      year: '',
      licensePlate: '',
      vin: '',
      mileage: '',
      fuelType: 'gasoline',
      status: 'active',
    });
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6 text-gray-800 dark:text-white">Add New Vehicle</h1>
      
      <form onSubmit={handleSubmit} className="max-w-2xl mx-auto">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Make */}
            <div>
              <label htmlFor="make" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Make
              </label>
              <input
                type="text"
                id="make"
                name="make"
                value={formData.make}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                placeholder="e.g., Toyota"
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
                placeholder="e.g., Camry"
              />
            </div>

            {/* Year */}
            <div>
              <label htmlFor="year" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Year
              </label>
              <input
                type="number"
                id="year"
                name="year"
                value={formData.year}
                onChange={handleChange}
                required
                min="1900"
                max={new Date().getFullYear() + 1}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                placeholder="e.g., 2023"
              />
            </div>

            {/* License Plate */}
            <div>
              <label htmlFor="licensePlate" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                License Plate
              </label>
              <input
                type="text"
                id="licensePlate"
                name="licensePlate"
                value={formData.licensePlate}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                placeholder="e.g., ABC123"
              />
            </div>

            {/* VIN */}
            <div>
              <label htmlFor="vin" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                VIN
              </label>
              <input
                type="text"
                id="vin"
                name="vin"
                value={formData.vin}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                placeholder="Vehicle Identification Number"
              />
            </div>

            {/* Mileage */}
            <div>
              <label htmlFor="mileage" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Current Mileage
              </label>
              <input
                type="number"
                id="mileage"
                name="mileage"
                value={formData.mileage}
                onChange={handleChange}
                required
                min="0"
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                placeholder="e.g., 50000"
              />
            </div>

            {/* Fuel Type */}
            <div>
              <label htmlFor="fuelType" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Fuel Type
              </label>
              <select
                id="fuelType"
                name="fuelType"
                value={formData.fuelType}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              >
                <option value="gasoline">Gasoline</option>
                <option value="diesel">Diesel</option>
                <option value="electric">Electric</option>
                <option value="hybrid">Hybrid</option>
              </select>
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
                <option value="active">Active</option>
                <option value="maintenance">In Maintenance</option>
                <option value="retired">Retired</option>
              </select>
            </div>
          </div>

          {/* Submit Button */}
          <div className="flex justify-end mt-6">
            <button
              type="submit"
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
            >
              Add Vehicle
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
