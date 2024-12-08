from ortools.sat.python import cp_model

# Import datetime utilities for handling dates and times
from datetime import datetime, timedelta
from typing import List

# Import our custom models that represent maintenance-related database tables
from eyefleet.apps.maintenance.models import Maintenance, Mechanic, MaintenanceBay, MaintenanceWindow, MaintenanceSchedule


# Main class that handles scheduling maintenance tasks
class MaintenanceScheduler:
    def __init__(self, start_date: datetime, end_date: datetime):
    
        # Store the date range we want to schedule maintenance for
        self.start_date = start_date
        self.end_date = end_date

        # Create a new constraint programming model
        self.model = cp_model.CpModel()
        # Create a solver that will find solutions to our model
        self.solver = cp_model.CpSolver()

    def create_variables(self, maintenances: List[Maintenance], mechanics: List[Mechanic], bays: List[MaintenanceBay]):
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

    def _add_assignment_constraints(self):
        """Each maintenance task must be assigned exactly once"""
        for maintenance in Maintenance.objects.all():
            task_vars = []
            for var_name, var in self.maintenance_vars.items():
                if str(maintenance.id) in var_name:
                    task_vars.append(var)
            # Sum of all assignments for this task must equal 1
            self.model.Add(sum(task_vars) == 1)

    def _add_mechanic_constraints(self):
        """Mechanics can't be assigned multiple tasks at the same time"""
        for mechanic in Mechanic.objects.all():
            for time_slot in self._generate_time_slots():
                mechanic_vars = []
                for var_name, var in self.maintenance_vars.items():
                    if str(mechanic.id) in var_name and str(time_slot) in var_name:
                        mechanic_vars.append(var)
                # Sum of assignments for this mechanic at this time must be <= 1
                self.model.Add(sum(mechanic_vars) <= 1)

    def _add_bay_constraints(self):
        """Maintenance bays can't have multiple tasks at the same time"""
        for bay in MaintenanceBay.objects.all():
            for time_slot in self._generate_time_slots():
                bay_vars = []
                for var_name, var in self.maintenance_vars.items():
                    if str(bay.id) in var_name and str(time_slot) in var_name:
                        bay_vars.append(var)
                # Sum of assignments for this bay at this time must be <= 1
                self.model.Add(sum(bay_vars) <= 1)

    def _add_window_constraints(self):
        """Tasks must be scheduled within allowed maintenance windows"""
        for maintenance in Maintenance.objects.all():
            for var_name, var in self.maintenance_vars.items():
                if str(maintenance.id) in var_name:
                    time_slot = self._extract_time_slot(var_name)
                    window = MaintenanceWindow.objects.filter(
                        day_of_week=time_slot.weekday()
                    ).first()
                    
                    if not window or (
                        time_slot.time() < window.start_time or 
                        time_slot.time() >= window.end_time
                    ):
                        # If outside window, this assignment must be 0
                        self.model.Add(var == 0)

    def _add_skill_constraints(self):
        """Mechanics must have required skills for assigned tasks"""
        for maintenance in Maintenance.objects.all():
            for mechanic in Mechanic.objects.all():
                required_skills = maintenance.required_skills.all()
                mechanic_skills = mechanic.skills.all()
                
                # If mechanic lacks any required skill
                if not all(skill in mechanic_skills for skill in required_skills):
                    # Find all variables involving this maintenance-mechanic pair
                    for var_name, var in self.maintenance_vars.items():
                        if (str(maintenance.id) in var_name and 
                            str(mechanic.id) in var_name):
                            # This assignment must be 0
                            self.model.Add(var == 0)

    def _add_priority_constraints(self):
        """Higher priority tasks should be scheduled earlier"""
        for maintenance in Maintenance.objects.all():
            priority_weight = self._get_priority_weight(maintenance.priority)
            
            for var_name, var in self.maintenance_vars.items():
                if str(maintenance.id) in var_name:
                    time_slot = self._extract_time_slot(var_name)
                    # Add soft constraint - higher cost for later slots
                    time_penalty = (time_slot - self.start_date).total_seconds() / 3600
                    self.model.Add(var * time_penalty * priority_weight)

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

    def _generate_time_slots(self):
        """Generate all possible time slots between start_date and end_date"""
        time_slots = []
        current_date = self.start_date
        
        # Generate slots for each day
        while current_date <= self.end_date:
            # Get maintenance windows for this day
            day_windows = MaintenanceWindow.objects.filter(
                day_of_week=current_date.weekday()
            )
            
            # For each maintenance window on this day
            for window in day_windows:
                # Create datetime objects for window start and end times
                window_start = datetime.combine(current_date, window.start_time)
                window_end = datetime.combine(current_date, window.end_time)
                
                # Generate hourly slots within this window
                current_slot = window_start
                while current_slot < window_end:
                    time_slots.append(current_slot)
                    current_slot += timedelta(hours=1)
            
            # Move to next day
            current_date += timedelta(days=1)
            
        return time_slots

    def _extract_time_slot(self, var_name: str) -> datetime:
        """Extract the time slot from a variable name
        
        Variable names are in format: maintenance_<id>_<id>_<id>_<datetime>
        The datetime is the last component after splitting on underscores
        """
        # Split the variable name and get the datetime string
        datetime_str = var_name.split('_')[-1]
        # Convert string back to datetime object
        return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

    def _get_priority_weight(self, priority: str) -> float:
        """Convert priority level to a numerical weight for optimization
        
        Higher priority tasks get lower weights (since we're minimizing cost)
        This makes them more likely to be scheduled earlier
        """
        priority_weights = {
            'critical': 0.25,  # Highest priority - lowest weight
            'high': 0.5,
            'medium': 1.0,
            'low': 2.0        # Lowest priority - highest weight
        }
        return priority_weights.get(priority, 1.0)  # Default to medium priority weight

    def _extract_maintenance_id(self, var_name: str) -> str:
        """Extract the maintenance ID from a variable name
        
        Variable names are in format: maintenance_<maintenance_id>_<mechanic_id>_<bay_id>_<datetime>
        The maintenance ID is the first component after 'maintenance_'
        """
        # Split the variable name and get the maintenance ID
        return var_name.split('_')[1]

    def _extract_mechanic_id(self, var_name: str) -> str:
        """Extract the mechanic ID from a variable name
        
        Variable names are in format: maintenance_<maintenance_id>_<mechanic_id>_<bay_id>_<datetime>
        The mechanic ID is the second component after 'maintenance_'
        """
        # Split the variable name and get the mechanic ID
        return var_name.split('_')[2]

    def _extract_bay_id(self, var_name: str) -> str:
        """Extract the bay ID from a variable name
        
        Variable names are in format: maintenance_<maintenance_id>_<mechanic_id>_<bay_id>_<datetime>
        The bay ID is the third component after 'maintenance_'
        """
        # Split the variable name and get the bay ID
        return var_name.split('_')[3]

    def _calculate_end_time(self, maintenance_id: str, start_time: datetime) -> datetime:
        """Calculate the end time for a maintenance task based on its estimated duration
        
        Args:
            maintenance_id: ID of the maintenance task
            start_time: Start time of the maintenance task
            
        Returns:
            datetime: End time of the maintenance task
        """
        maintenance = Maintenance.objects.get(id=maintenance_id)
        # Add the estimated duration (in hours) to the start time
        return start_time + timedelta(hours=maintenance.estimated_duration)

    def _calculate_cost(self, maintenance_id: str, mechanic_id: str) -> float:
        """Calculate the estimated cost for a maintenance task
        
        Args:
            maintenance_id: ID of the maintenance task
            mechanic_id: ID of the assigned mechanic
            
        Returns:
            float: Estimated cost of the maintenance task
        """
        maintenance = Maintenance.objects.get(id=maintenance_id)
        mechanic = Mechanic.objects.get(id=mechanic_id)
        
        # Base cost is mechanic's hourly rate times estimated duration
        base_cost = mechanic.hourly_rate * maintenance.estimated_duration
        
        # Adjust for mechanic's efficiency
        adjusted_cost = base_cost / mechanic.efficiency_rating
        
        # Add any additional costs (parts, materials, etc.)
        total_cost = adjusted_cost + maintenance.additional_costs
        
        return total_cost