export interface Vehicle {
  id?: number;
  make: string;
  model: string;
  year: number;
  registration: string;
  vin: string;
  status: 'active' | 'maintenance' | 'inactive';
}

export interface VehicleFormData {
  make: string;
  model: string;
  year: number;
  registration: string;
  vin: string;
  status: 'active' | 'maintenance' | 'inactive';
}
