import factory
from factory.django import DjangoModelFactory
from faker import Faker
from django.utils import timezone
from decimal import Decimal
from eyefleet.apps.livetracking.models.devices import Device, DeviceConfiguration, DEVICE_TYPE_CHOICES, DEVICE_STATUS_CHOICES

fake = Faker()

class DeviceConfigurationFactory(DjangoModelFactory):
    class Meta:
        model = DeviceConfiguration

    name = factory.Faker('word')
    description = factory.Faker('sentence')
    device_type = factory.Iterator([choice[0] for choice in DEVICE_TYPE_CHOICES])
    firmware_version = factory.Faker('numerify', text='v#.#.#')
    settings = factory.Dict({
        'setting1': factory.LazyFunction(
            lambda: str(fake.pydecimal(left_digits=3, right_digits=2))
        ),
        'setting2': factory.LazyFunction(
            lambda: str(fake.pydecimal(left_digits=2, right_digits=2))
        ),
    })

class DeviceFactory(DjangoModelFactory):
    class Meta:
        model = Device

    name = factory.Faker('word')
    ip_address = factory.Faker('ipv4')
    connected = factory.Faker('boolean')
    last_pinged = factory.LazyFunction(timezone.now)
    status = factory.Iterator([choice[0] for choice in DEVICE_STATUS_CHOICES])
    @factory.lazy_attribute
    def location(self):
        # Birmingham's approximate bounds
        return {
            'latitude': str(Decimal(str(fake.latitude(
                # min_value=52.381,    # Southern Birmingham
                # max_value=52.561     # Northern Birmingham
            )))),
            'longitude': str(Decimal(str(fake.longitude(
                # min_value=-2.022,    # Western Birmingham
                # max_value=-1.728     # Eastern Birmingham
            ))))
        }
    battery_level = factory.Faker('random_int', min=0, max=100)
    configuration = factory.SubFactory(DeviceConfigurationFactory)
    assigned_vehicle = factory.Faker('word')