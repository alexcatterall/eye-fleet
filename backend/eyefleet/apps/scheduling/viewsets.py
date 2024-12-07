from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from eyefleet.apps.scheduling.models import (
    Mission,
    MissionAssignedEmployee,
    MissionSchedule,
    Trip,
    Cargo
)
from eyefleet.apps.scheduling.serializers import (
    MissionSerializer,
    MissionAssignedEmployeeSerializer,
    MissionScheduleSerializer,
    TripSerializer,
    CargoSerializer
)

class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'priority']
    search_fields = ['id', 'name', 'description']


    @action(detail=False, methods=['post'])
    def optimize_schedules(self, request):
        """Optimize mission schedules based on available assets"""
        try:
            # Get parameters from request
            start_date = datetime.fromisoformat(request.data.get('start_date'))
            end_date = datetime.fromisoformat(request.data.get('end_date'))
            mission_ids = request.data.get('mission_ids', [])
            
            # Get missions and available assets
            missions = Mission.objects.filter(
                id__in=mission_ids,
                status='active'
            )
            available_assets = Asset.objects.filter(
                status='available'
            )
            
            if not missions or not available_assets:
                return Response(
                    {'error': 'No missions or available assets found'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Run optimization
            optimizer = MissionOptimizer()
            result = optimizer.optimize_mission_schedules(
                missions=missions,
                available_assets=available_assets,
                time_window_start=start_date,
                time_window_end=end_date
            )
            
            if result is None:
                return Response(
                    {'error': 'No feasible solution found'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(detail=False, methods=['post'])
    def create_schedule(self, request):
        """Create new schedule for missions"""
        try:
            start_date = datetime.fromisoformat(request.data.get('start_date'))
            end_date = datetime.fromisoformat(request.data.get('end_date'))
            recurrence_type = request.data.get('recurrence_type')
            mission_ids = request.data.get('mission_ids', [])

            scheduler = MissionScheduler()
            result = scheduler.schedule_missions(
                start_date=start_date,
                end_date=end_date,
                recurrence_type=recurrence_type,
                mission_ids=mission_ids
            )

            if 'error' in result:
                return Response(
                    {'error': result['error']},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(result, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def optimize_route(self, request, pk=None):
        """Optimize route for a specific schedule"""
        try:
            schedule = self.get_object()
            scheduler = MissionScheduler()
            
            result = scheduler.optimize_mission_route(
                mission=schedule.reference_mission,
                schedule=schedule
            )

            if not result:
                return Response(
                    {'error': 'Could not optimize route'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def process_recurring(self, request):
        """Process all recurring schedules"""
        try:
            scheduler = MissionScheduler()
            scheduler.process_recurring_schedules()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class MissionAssignedEmployeeViewSet(viewsets.ModelViewSet):
    queryset = MissionAssignedEmployee.objects.all()
    serializer_class = MissionAssignedEmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['mission', 'role']
    search_fields = ['id']

class MissionScheduleViewSet(viewsets.ModelViewSet):
    queryset = MissionSchedule.objects.all()
    serializer_class = MissionScheduleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id']

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['id']

class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['mission']
    search_fields = ['id', 'description']