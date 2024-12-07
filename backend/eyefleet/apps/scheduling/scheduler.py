# Import necessary libraries
# cp_model is a constraint programming solver from Google's OR-Tools
from ortools.sat.python import cp_model

# Import typing hints to help with code readability and error checking
from typing import List, Dict, Tuple

# Import date/time utilities for handling schedules
from datetime import datetime, timedelta

# Import Django's timezone utilities for handling timezone-aware dates
from django.utils import timezone

# Import our custom models that represent database tables
from .models.missions import Mission
from .models.schedules import MissionSchedule
from .models.cargo import Cargo
from eyefleet.apps.maintenance.models.assets import Asset

# Main class for optimizing mission schedules
class MissionOptimizer:
    def __init__(self):
        # Create a new constraint programming model and solver when initialized
        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()

    def optimize_mission_schedules(
        self,
        missions: List[Mission],  # List of missions that need scheduling
        available_assets: List[Asset],  # List of vehicles/assets available
        time_window_start: datetime,  # When scheduling period starts
        time_window_end: datetime,  # When scheduling period ends
        max_mission_duration: int = 480  # Maximum mission length (8 hours in minutes)
    ) -> Dict[str, List[Dict]]:
        """
        This method takes missions and tries to schedule them optimally with available assets.
        It returns a dictionary with the optimized schedules.
        """
        
        # Convert the time window to minutes for easier calculations
        horizon = int((time_window_end - time_window_start).total_seconds() / 60)
        
        # Create dictionaries to store our decision variables
        mission_starts = {}  # When each mission starts
        mission_ends = {}    # When each mission ends
        mission_assets = {}  # Which asset is assigned to each mission
        
        # For each mission, create variables to track start time, end time, and assigned asset
        for mission in missions:
            # Create variable for mission start time (can be anywhere from 0 to horizon)
            mission_starts[mission.id] = self.model.NewIntVar(
                0, horizon, f'start_{mission.id}'
            )
            
            # Create variable for mission end time
            mission_ends[mission.id] = self.model.NewIntVar(
                0, horizon, f'end_{mission.id}'
            )
            
            # Create variable for asset assignment (can be any available asset)
            mission_assets[mission.id] = self.model.NewIntVar(
                0, len(available_assets) - 1, f'asset_{mission.id}'
            )

        # Add constraints to make sure schedules are feasible

        # 1. Make sure missions don't exceed maximum duration
        for mission in missions:
            self.model.Add(
                mission_ends[mission.id] - mission_starts[mission.id] <= max_mission_duration
            )
            self.model.Add(mission_ends[mission.id] > mission_starts[mission.id])

        # 2. Make sure missions using the same asset don't overlap
        for i, mission1 in enumerate(missions):
            for mission2 in missions[i + 1:]:
                # Create variable to track if missions use same asset
                asset_same = self.model.NewBoolVar('asset_same')
                self.model.Add(
                    mission_assets[mission1.id] == mission_assets[mission2.id]
                ).OnlyEnforceIf(asset_same)
                
                # Create variable to track if missions don't overlap
                no_overlap = self.model.NewBoolVar('no_overlap')
                self.model.Add(
                    mission_ends[mission1.id] <= mission_starts[mission2.id]
                ).OnlyEnforceIf(no_overlap)
                self.model.Add(
                    mission_ends[mission2.id] <= mission_starts[mission1.id]
                ).OnlyEnforceIf(no_overlap.Not())
                
                # If missions use same asset, they cannot overlap
                self.model.AddImplication(asset_same, no_overlap)

        # 3. Make sure assets are capable of handling assigned missions
        for mission in missions:
            for i, asset in enumerate(available_assets):
                if not self._check_asset_capability(mission, asset):
                    self.model.Add(mission_assets[mission.id] != i)

        # Set objective: Try to complete all missions as early as possible
        max_completion = self.model.NewIntVar(0, horizon, 'max_completion')
        for mission in missions:
            self.model.Add(max_completion >= mission_ends[mission.id])
        self.model.Minimize(max_completion)

        # Try to solve the optimization problem
        status = self.solver.Solve(self.model)
        
        # If we found a solution, create and return the schedules
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            return self._create_schedule_output(
                missions,
                available_assets,
                mission_starts,
                mission_ends,
                mission_assets,
                time_window_start
            )
        
        # If no solution found, return None
        return None

    def _check_asset_capability(self, mission: Mission, asset: Asset) -> bool:
        """
        Check if an asset can handle a mission by comparing cargo weight/volume
        to asset capacity
        """
        # Calculate total weight and volume of all cargo in the mission
        total_cargo_weight = sum(cargo.weight or 0 for cargo in mission.cargos.all())
        total_cargo_volume = sum(cargo.volume or 0 for cargo in mission.cargos.all())
        
        # Return True if asset can handle the mission
        return (
            asset.status == 'available' and
            asset.capacity_weight >= total_cargo_weight and
            asset.capacity_volume >= total_cargo_volume
        )

    def _create_schedule_output(
        self,
        missions: List[Mission],
        available_assets: List[Asset],
        mission_starts: Dict,
        mission_ends: Dict,
        mission_assets: Dict,
        time_window_start: datetime
    ) -> Dict[str, List[Dict]]:
        """
        Convert the optimization results into actual schedule objects in the database
        """
        schedules = []
        
        # For each mission, create a schedule with the optimized times and asset
        for mission in missions:
            # Calculate actual start and end times
            start_time = time_window_start + timedelta(
                minutes=self.solver.Value(mission_starts[mission.id])
            )
            end_time = time_window_start + timedelta(
                minutes=self.solver.Value(mission_ends[mission.id])
            )
            # Get the assigned asset
            assigned_asset = available_assets[
                self.solver.Value(mission_assets[mission.id])
            ]
            
            # Create a new schedule in the database
            schedule = MissionSchedule.objects.create(
                reference_mission=mission,
                vehicle=assigned_asset,
                start_time=start_time.time(),
                end_time=end_time.time(),
                status='scheduled',
                estimated_duration=str(end_time - start_time),
                deliveries=mission.stops,
                total_stops=mission.stops
            )
            
            # Associate cargos with the schedule
            schedule.cargos.set(mission.cargos.all())
            
            # Add schedule details to our results
            schedules.append({
                'schedule_id': schedule.id,
                'mission_id': mission.id,
                'asset_id': assigned_asset.id,
                'start_time': start_time,
                'end_time': end_time,
                'duration_minutes': self.solver.Value(
                    mission_ends[mission.id] - mission_starts[mission.id]
                )
            })
            
        # Return all schedules with optimization status
        return {
            'status': 'optimal' if self.solver.StatusName() == 'OPTIMAL' else 'feasible',
            'schedules': schedules
        }
    

# Import libraries for route optimization
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from typing import List, Dict, Tuple
import numpy as np
from datetime import datetime, timedelta
from dataclasses import dataclass
import googlemaps  # For calculating real driving distances/times
from django.conf import settings

# Define a class to represent each stop on a route
@dataclass
class Stop:
    id: str
    location: Dict[str, float]  # Latitude/longitude coordinates
    time_window: Tuple[int, int]  # When customer wants delivery
    service_time: int  # How long it takes to service this stop
    demand: float  # How much cargo needs to be delivered

# Class for optimizing the sequence of stops on a route
class RoutePathOptimizer:
    def __init__(self, api_key: str = settings.GOOGLE_MAPS_API_KEY):
        """Set up Google Maps client for distance calculations"""
        self.gmaps = googlemaps.Client(key=api_key)

    def optimize_route(
        self,
        depot_location: Dict[str, float],  # Where vehicles start/end
        stops: List[Stop],  # List of stops to visit
        vehicle_capacity: float,  # How much the vehicle can carry
        max_route_duration: int = 480,  # Maximum route length (8 hours)
        start_time: datetime = None  # When route should start
    ) -> Dict:
        """
        Find the best order to visit stops while respecting all constraints
        """
        # Get the driving times/distances between all locations
        locations = [depot_location] + [stop.location for stop in stops]
        distance_matrix, time_matrix = self._create_distance_matrix(locations)

        # Set up the routing problem
        manager = pywrapcp.RoutingIndexManager(
            len(locations),
            1,  # Number of vehicles
            0   # Starting location (depot)
        )
        routing = pywrapcp.RoutingModel(manager)

        # Create function to look up travel times between stops
        def time_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return time_matrix[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(time_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Create function to look up how much cargo is at each stop
        def demand_callback(from_index):
            from_node = manager.IndexToNode(from_index)
            if from_node == 0:  # Depot has no demand
                return 0
            return stops[from_node - 1].demand

        # Add vehicle capacity constraint
        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # No slack
            [vehicle_capacity],  # Maximum vehicle capacity
            True,  # Start empty
            'Capacity'
        )

        # Add time constraints
        time_dimension_name = 'Time'
        routing.AddDimension(
            transit_callback_index,
            30,  # Allow waiting up to 30 minutes at stops
            max_route_duration,  # Maximum route duration
            False,  # Don't force start at time 0
            time_dimension_name
        )
        time_dimension = routing.GetDimensionOrDie(time_dimension_name)

        # Add time windows for each stop
        for location_idx, stop in enumerate(stops, 1):
            index = manager.NodeToIndex(location_idx)
            time_dimension.CumulVar(index).SetRange(
                stop.time_window[0],
                stop.time_window[1]
            )

        # Add service times at stops
        for location_idx, stop in enumerate(stops, 1):
            index = manager.NodeToIndex(location_idx)
            routing.AddToAssignment(
                time_dimension.SlackVar(index)
            )
            time_dimension.SetSpanCostCoefficientForVehicle(100, 0)

        # Configure how to search for a solution
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        )
        search_parameters.time_limit.seconds = 30

        # Try to find optimal route
        solution = routing.SolveWithParameters(search_parameters)

        if not solution:
            return None

        # Convert solution into usable format
        return self._create_route_output(
            manager,
            routing,
            solution,
            stops,
            time_matrix,
            distance_matrix,
            start_time
        )

    def _create_distance_matrix(
        self,
        locations: List[Dict[str, float]]
    ) -> Tuple[List[List[int]], List[List[int]]]:
        """
        Use Google Maps to get actual driving distances/times between all locations
        """
        # Convert locations to strings for Google Maps API
        origins = [f"{loc['lat']},{loc['lng']}" for loc in locations]
        destinations = origins

        # Get distance matrix from Google Maps
        result = self.gmaps.distance_matrix(
            origins,
            destinations,
            mode="driving",
            departure_time="now"
        )

        # Create empty matrices
        num_locations = len(locations)
        distance_matrix = [[0] * num_locations for _ in range(num_locations)]
        time_matrix = [[0] * num_locations for _ in range(num_locations)]

        # Fill matrices with results from Google Maps
        for i, row in enumerate(result['rows']):
            for j, element in enumerate(row['elements']):
                if element['status'] == 'OK':
                    distance_matrix[i][j] = element['distance']['value']  # meters
                    time_matrix[i][j] = element['duration']['value'] // 60  # minutes

        return distance_matrix, time_matrix

    def _create_route_output(
        self,
        manager,
        routing,
        solution,
        stops: List[Stop],
        time_matrix: List[List[int]],
        distance_matrix: List[List[int]],
        start_time: datetime
    ) -> Dict:
        """
        Convert the solution into a list of stops with arrival/departure times
        """
        route = []
        index = routing.Start(0)
        current_time = 0
        total_distance = 0
        
        # Follow the route stop by stop
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            next_index = solution.Value(routing.NextVar(index))
            next_node_index = manager.IndexToNode(next_index)
            
            # If this isn't the depot, add stop to route
            if node_index != 0:
                stop = stops[node_index - 1]
                arrival_time = current_time
                
                route.append({
                    'stop_id': stop.id,
                    'location': stop.location,
                    'arrival_time': (
                        start_time + timedelta(minutes=arrival_time)
                        if start_time else arrival_time
                    ),
                    'departure_time': (
                        start_time + timedelta(minutes=arrival_time + stop.service_time)
                        if start_time else arrival_time + stop.service_time
                    ),
                    'service_time': stop.service_time,
                    'demand': stop.demand
                })
                
                current_time += stop.service_time
            
            # Add travel time to next stop
            if not routing.IsEnd(next_index):
                total_distance += distance_matrix[node_index][next_node_index]
                current_time += time_matrix[node_index][next_node_index]
            
            index = next_index

        # Return complete route information
        return {
            'status': 'optimal',
            'total_distance': total_distance,  # meters
            'total_time': current_time,  # minutes
            'route': route
        }

    def optimize_multiple_routes(
        self,
        depot_location: Dict[str, float],
        all_stops: List[Stop],
        vehicle_capacities: List[float],
        max_route_duration: int = 480,
        start_times: List[datetime] = None
    ) -> List[Dict]:
        """
        Future method to handle multiple vehicles/routes
        (Not implemented yet)
        """
        pass


# Class that combines mission optimization and route optimization
class MissionScheduler:
    def __init__(self):
        # Create optimizers when initialized
        self.optimizer = MissionOptimizer()
        self.route_optimizer = RoutePathOptimizer()

    def optimize_mission_route(
        self,
        mission: Mission,
        schedule: MissionSchedule
    ) -> Dict:
        """
        Take a mission and its schedule and optimize the route between stops
        """
        # Convert mission stops into format route optimizer can use
        stops = []
        for stop_point in mission.stop_points:
            stops.append(Stop(
                id=str(stop_point.get('id', '')),
                location=stop_point.get('location', {}),
                time_window=(
                    self._convert_time_to_minutes(schedule.start_time),
                    self._convert_time_to_minutes(schedule.end_time)
                ),
                service_time=30,  # Default 30 minutes at each stop
                demand=stop_point.get('demand', 0)
            ))

        # Get starting location
        depot_location = mission.stop_points[0]['location']

        # Get vehicle capacity
        vehicle_capacity = schedule.vehicle.capacity_weight

        # Find optimal route
        optimized_route = self.route_optimizer.optimize_route(
            depot_location=depot_location,
            stops=stops,
            vehicle_capacity=vehicle_capacity,
            max_route_duration=480,  # 8 hours
            start_time=datetime.combine(
                timezone.now().date(),
                schedule.start_time
            )
        )

        # If route found, update schedule
        if optimized_route:
            schedule.stop_points = [stop for stop in optimized_route['route']]
            schedule.estimated_duration = str(
                timedelta(minutes=optimized_route['total_time'])
            )
            schedule.save()

        return optimized_route

    def _convert_time_to_minutes(self, time_obj) -> int:
        """
        Convert time to minutes since start of day
        Example: 2:30 PM = (14 * 60) + 30 = 870 minutes
        """
        return time_obj.hour * 60 + time_obj.minute