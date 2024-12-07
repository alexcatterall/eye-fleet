from ortools.sat.python import cp_model
from datetime import datetime, timedelta

from eyefleet.apps.scheduling.models import Maintenance, Maintainer, MaintenanceBay, MaintenanceWindow



class MaintenanceScheduler:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()

    def create_variables(self, maintenances, mechanics, bays):
        """create decision variables for the optimization problem"""
        self.maintenance_vars = {}
        time_slots = self._generate_time_slots()

        for maintenance in maintenances:
            for mechanic in mechanics:
                for bay in bays:
                    for slot in time_slots:
                        var_name  = f'maintenance_{maintenance.id}_{mechanic.id}_{bay.id}_{slot}'
                        self.maintenance_vars[var_name] = self.model.NewBoolVar(var_name)
    
    def add_constraints(self):
        """add constraints to the optimization problem"""
        self._add_assignment_constraints()

        self._add_mechanic_constraints()

        self._add_bay_constraints()

        self._add_window_constraints()

        self._add_skill_constraints()

        self._add_priority_constraints()

    def optimize(self):
        """ solve the optimization problem"""
        self.model.Minimize(self._objective_function())
        status = self.solver.Solve(self.model)

        if status == cp_model.OPTIMAL:
            return self._create_schedule()
        return None

    def _objective_function(self):
        """define the optimization objective"""
        total_cost = 0
        for var_name, var in self.maintenance_vars.items():
            maintenance_id = self._extract_maintenance_id(var_name)
            mechanic_id = self._extract_mechanic_id(var_name)
            
            maintenance = Maintenance.objects.get(id=maintenance_id)
            mechanic = Mechanic.objects.get(id=mechanic_id)
            
            # Cost components
            labor_cost = mechanic.hourly_rate * maintenance.estimated_duration
            priority_weight = self._get_priority_weight(maintenance.priority)
            efficiency = mechanic.efficiency_rating
            
            total_cost += var * (labor_cost * priority_weight / efficiency)
        
        return total_cost
    
    def _create_schedule(self):
        """create a schedule from the solution"""
        for var_name, var in self.maintenance_vars.items():
            if self.solver.Value(var):
                maintenance_id = self._extract_maintenance_id(var_name)
                mechanic_id = self._extract_mechanic_id(var_name)
                bay_id = self._extract_bay_id(var_name)
                time_slot = self._extract_time_slot(var_name)
                
                schedule = MaintenanceSchedule.objects.create(
                    maintenance_id=maintenance_id,
                    mechanic_id=mechanic_id,
                    bay_id=bay_id,
                    start_time=time_slot,
                    end_time=self._calculate_end_time(maintenance_id, time_slot),
                    estimated_cost=self._calculate_cost(maintenance_id, mechanic_id)
                )
                schedules.append(schedule)
        
        return schedules