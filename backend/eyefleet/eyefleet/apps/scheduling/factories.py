import factory
from factory.django import DjangoModelFactory
import random
from faker import Faker
from django.utils import timezone
from datetime import timedelta

from telemex.apps.routes.models import (Trip, TripStatus, Route, RouteStatus, RoutePriority, 
                                        CargoType, CargoStatus, CargoPriority, Cargo, RouteScheduleStatus, RouteScheduleShift, RouteScheduleRecurrence, RouteSchedule)
from telemex.apps.vehicles.models import Vehicle

fake = Faker()

class TripFactory(DjangoModelFactory):
    class Meta:
        model = Trip

    reference_route = factory.Sequence(lambda n: f'ROUTE-{n:04d}')
    
    # Generate start_time within last 30 days
    start_time = factory.LazyFunction(
        lambda: timezone.now() - timedelta(days=random.randint(0, 30))
    )
    
    # End time 1-8 hours after start_time
    end_time = factory.LazyAttribute(
        lambda o: o.start_time + timedelta(hours=random.uniform(1, 8))
    )
    
    source = factory.Faker('city')
    destination = factory.Faker('city')
    driver = factory.Faker('name')
    vehicle = factory.Iterator(Vehicle.objects.all())    
    # Generate random staff and passengers lists
    staff = factory.LazyFunction(
        lambda: [{ "name" : fake.name() } for _ in range(random.randint(0, 10))]
    )
    passengers = factory.LazyFunction(
        lambda: [{ "name" : fake.name() } for _ in range(random.randint(0, 10))]
    )
    
    on_time = factory.Faker('boolean', chance_of_getting_true=70)
    progress = factory.LazyFunction(lambda: random.randint(0, 100))
    
    status = factory.Iterator(TripStatus.objects.all())

class CargoFactory(DjangoModelFactory):
    class Meta:
        model = Cargo
    
    type = factory.Iterator(CargoType.objects.all())
    status = factory.Iterator(CargoStatus.objects.all())

    weight = factory.Faker('random_int', min=1000, max=100000)
    volume = factory.Faker('random_int', min=1000, max=100000)

    description = factory.Faker('sentence')
    name = factory.Faker('word')

    pickup_point = factory.Faker('city')
    dropoff_point = factory.Faker('city')

    expected_pickup_t = factory.Faker('date_time_between', start_date='-30d', end_date='now')
    expected_dropoff_t = factory.Faker('date_time_between', start_date='-30d', end_date='now')

    has_return = factory.Faker('boolean', chance_of_getting_true=50)
    special_instructions = factory.LazyFunction(
        lambda: [{ "instruction" : fake.sentence() } for _ in range(random.randint(0, 5))]
    )

    priority = factory.Iterator(CargoPriority.objects.all())
    sender = factory.Faker('name')
    receiver = factory.Faker('name')
    handler = factory.Faker('name')

class RouteFactory(DjangoModelFactory):
    class Meta:
        model = Route

    route_number = factory.Sequence(lambda n: f'ROUTE-{n:04d}')
    driver = factory.Faker('name')
    vehicle = factory.Faker('word')

    stops = factory.Faker('random_int', min=1, max=10)
    description = factory.Faker('sentence')
    notes = factory.Faker('paragraph')
    
    status = factory.Iterator(RouteStatus.objects.all())
    priority = factory.Iterator(RoutePriority.objects.all())

    @factory.lazy_attribute
    def stop_points(self):
        return [{"location": fake.city(), "arrival_time": fake.date_time_between(start_date='-30d', end_date='now')} for _ in range(self.stops)]
    
    total_weight = 0
    total_volume = 0


    @factory.post_generation
    def cargos(self, create, extracted, **kwargs):
        if not create:
            return
        route_cargos = []
        if extracted:
            for cargo in extracted:
                self.cargos.add(cargo)
                route_cargos.append(cargo)
        else:
            # create one cargo per stop
            created_cargos = CargoFactory.create_batch(self.stops)

            for cargo in created_cargos:
                self.cargos.add(cargo)
                route_cargos.append(cargo)

        # update route totals
        self.total_weight = sum(cargo.weight for cargo in route_cargos)
        self.total_volume = sum(cargo.volume for cargo in route_cargos)
        self.save()

class RouteScheduleFactory(DjangoModelFactory):
    class Meta:
        model = RouteSchedule
    
    shift = factory.Iterator(RouteScheduleShift.objects.all())
    reference_route = factory.Iterator(Route.objects.all())

    driver = factory.Faker('name')
    vehicle = factory.Iterator(Vehicle.objects.all())

    status = factory.Iterator(RouteScheduleStatus.objects.all())

    start_time = factory.Faker('date_time_between', start_date='-30d', end_date='now')
    end_time = factory.Faker('date_time_between', start_date='-30d', end_date='now')

    deliveries = factory.Faker('random_int', min=1, max=10)

    estimated_duration = factory.Faker('time')

    notes = factory.Faker('paragraph')
    actual_duration = factory.Faker('time')
    total_stops = factory.Faker('random_int', min=1, max=10)

    @factory.lazy_attribute
    def stop_points(self):
        return [{"location": fake.city(), "arrival_time": fake.date_time_between(start_date='-30d', end_date='now')} for _ in range(self.stops)]
    

    @factory.post_generation
    def cargos(self, create, extracted, **kwargs):
        if not create:
            return
        route_cargos = []
        if extracted:
            for cargo in extracted:
                self.cargos.add(cargo)
                route_cargos.append(cargo)
        else:
            # create one cargo per stop
            created_cargos = CargoFactory.create_batch(self.stops)

            for cargo in created_cargos:
                self.cargos.add(cargo)
                route_cargos.append(cargo)

        # update route totals
        self.total_weight = sum(cargo.weight for cargo in route_cargos)
        self.total_volume = sum(cargo.volume for cargo in route_cargos)
        self.save()

