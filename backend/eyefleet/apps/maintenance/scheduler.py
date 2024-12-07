# Import the constraint programming solver from Google OR-Tools library
from ortools.sat.python import cp_model
# Import datetime utilities for handling dates and times
from datetime import datetime, timedelta

# Import our custom models that represent maintenance-related database tables
from eyefleet.apps.scheduling.models import Maintenance, Maintainer, MaintenanceBay, MaintenanceWindow


# Main class that handles scheduling maintenance tasks
class MaintenanceScheduler:
    def __init__(self, start_date, end_date):
        # Store the date range we want to schedule maintenance for
        self.start_date = start_date
        self.end_date = end_date
        # Create a new constraint programming model
        self.model = cp_model.CpModel()
        # Create a solver that will find solutions to our model
        self.solver = cp_model.CpSolver()

    def create_variables(self, maintenances, mechanics, bays):
        """create decision variables for the optimization problem"""
        # Dictionary to store all our decision variables
        self.maintenance_vars = {}
        # Get all possible time slots between start and end date
        time_slots = self._generate_time_slots()

        # Create a binary (yes/no) variable for every possible combination of:
        # maintenance task, mechanic, maintenance bay, and time slot
        for maintenance in maintenances:
            for mechanic in mechanics:
                for bay in bays:
                    for slot in time_slots:
                        # Create a unique name for this variable
                        var_name  = f'maintenance_{maintenance.id}_{mechanic.id}_{bay.id}_{slot}'
                        # Add a new binary variable to our model
                        self.maintenance_vars[var_name] = self.model.NewBoolVar(var_name)
    
    def add_constraints(self):
        """add constraints to the optimization problem"""
        # Make sure each maintenance task is assigned exactly once
        self._add_assignment_constraints()

        # Make sure mechanics aren't scheduled for multiple tasks at once
        self._add_mechanic_constraints()

        # Make sure maintenance bays aren't double-booked
        self._add_bay_constraints()

        # Make sure tasks are scheduled within their allowed time windows
        self._add_window_constraints()

        # Make sure mechanics have the right skills for their assigned tasks
        self._add_skill_constraints()

        # Handle priority levels for different maintenance tasks
        self._add_priority_constraints()

    def optimize(self):
        """solve the optimization problem"""
        # Tell the model to minimize our objective function (total cost)
        self.model.Minimize(self._objective_function())
        # Try to solve the model
        status = self.solver.Solve(self.model)

        # If we found an optimal solution, create and return the schedule
        if status == cp_model.OPTIMAL:
            return self._create_schedule()
        # If no solution found, return None
        return None

    def _objective_function(self):
        """define what we want to optimize (minimize) - in this case, total cost"""
        total_cost = 0
        # Look at each possible assignment in our variables
        for var_name, var in self.maintenance_vars.items():
            # Extract the IDs from the variable name
            maintenance_id = self._extract_maintenance_id(var_name)
            mechanic_id = self._extract_mechanic_id(var_name)
            
            # Look up the actual maintenance task and mechanic objects
            maintenance = Maintenance.objects.get(id=maintenance_id)
            mechanic = Mechanic.objects.get(id=mechanic_id)
            
            # Calculate cost components:
            # Base labor cost = mechanic's rate * how long the task takes
            labor_cost = mechanic.hourly_rate * maintenance.estimated_duration
            # Adjust cost based on task priority
            priority_weight = self._get_priority_weight(maintenance.priority)
            # Factor in mechanic's efficiency rating
            efficiency = mechanic.efficiency_rating
            
            # Add this assignment's cost to total (only counts if var is 1/True)
            total_cost += var * (labor_cost * priority_weight / efficiency)
        
        return total_cost
    
    def _create_schedule(self):
        """convert the mathematical solution into actual schedule entries"""
        # List to store all scheduled maintenance tasks
        schedules = []
        # Look at each variable in our solution
        for var_name, var in self.maintenance_vars.items():
            # If this variable is 1 (True) in our solution
            if self.solver.Value(var):
                # Extract all the details from the variable name
                maintenance_id = self._extract_maintenance_id(var_name)
                mechanic_id = self._extract_mechanic_id(var_name)
                bay_id = self._extract_bay_id(var_name)
                time_slot = self._extract_time_slot(var_name)
                
                # Create a new schedule entry in the database
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