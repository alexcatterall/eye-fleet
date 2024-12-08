import os
import pandas as pd
from influxdb_client import InfluxDBClient
from django.conf import settings
from llama_index.experimental.query_engine import PandasQueryEngine
from ..models import Device, Indicator





class LivetrackingTools:
    """Tools for livetracking data analysis and querying"""
    
    def __init__(self):
        self.influx_client = InfluxDBClient(
            url=settings.INFLUXDB_URL,
            token=settings.INFLUXDB_TOKEN,
            org=settings.INFLUXDB_ORG
        )
        self.query_api = self.influx_client.query_api()
        self.csv_path = "telemetry_data.csv"
        self.index = None
        
    def fetch_telemetry_data(self, device_id: str, indicator: str, 
                            hours: int = 24) -> pd.DataFrame:
        """Fetch recent telemetry data from InfluxDB"""
        query = f'''
        from(bucket: "{device_id.lower()}")
            |> range(start: -{hours}h)
            |> filter(fn: (r) => r["_measurement"] == "{indicator}")
            |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        '''
        
        result = self.query_api.query_data_frame(query)
        if result.empty:
            return pd.DataFrame()
            
        return result

    def generate_csv_dataset(self, max_rows: int = 100000) -> str:
        """Generate CSV file from recent telemetry data"""
        all_data = []
        
        # Fetch data for each device and indicator
        for device in Device.objects.all():
            for indicator in Indicator.objects.all():
                df = self.fetch_telemetry_data(device.id, indicator.name)
                if not df.empty:
                    df['device_id'] = device.id
                    df['indicator'] = indicator.name
                    all_data.append(df)
        
        if not all_data:
            return ""
            
        # Combine and truncate data
        combined_df = pd.concat(all_data)
        if len(combined_df) > max_rows:
            combined_df = combined_df.tail(max_rows)
            
        # Save to CSV
        combined_df.to_csv(self.csv_path, index=False)
        return self.csv_path

    def build_query_engine(self) -> PandasQueryEngine:
        """Build query engine from CSV data"""
        if not os.path.exists(self.csv_path):
            self.generate_csv_dataset()
            
        df = pd.read_csv(self.csv_path)
        return PandasQueryEngine(df=df)

    def query_telemetry(self, query: str) -> str:
        """Query telemetry data using natural language"""
        engine = self.build_query_engine()
        response = engine.query(query)
        return str(response)

    def analyze_patterns(self, device_id: str, indicator: str) -> str:
        """Analyze patterns in telemetry data"""
        df = self.fetch_telemetry_data(device_id, indicator, hours=168)  # 1 week
        if df.empty:
            return "No data available for analysis"
            
        # Perform basic statistical analysis
        stats = {
            "mean": df['value'].mean(),
            "std": df['value'].std(),
            "min": df['value'].min(),
            "max": df['value'].max()
        }
        
        return f"Analysis for {indicator} on {device_id}:\n" + \
               "\n".join([f"{k}: {v:.2f}" for k, v in stats.items()])

    def query_device_info(self, query: str) -> str:
        """Query device information using natural language when asked about devices use this tool"""
        # Convert Device queryset to DataFrame
        devices = Device.objects.all()
        device_data = [
            {
                'id': device.id,
                'name': device.name,
                'status': device.status,
                'ip_address': device.ip_address,
                'location': device.location,
                'battery_level': device.battery_level,
                'device_type': device.device_type,
                'firmware_version': device.firmware_version,
                'assigned_asset': device.assigned_asset,
                # Add other relevant device fields
            }
            for device in devices
        ]
        df = pd.DataFrame(device_data)
        
        # Create query engine and execute query
        engine = PandasQueryEngine(df=df)
        response = engine.query(query)
        return str(response)

    def query_data_indicator_info(self, query: str) -> str:
        """Query data indicator information using natural language when asked about indicators use this tool"""
        # Convert Indicator queryset to DataFrame
        indicators = Indicator.objects.all()
        indicator_data = [
            {
                'id': indicator.id,
                'name': indicator.name,
                'data_type': indicator.data_type,
                'min_value': indicator.min_value,
                'max_value': indicator.max_value,
            }
            for indicator in indicators
        ]
        df = pd.DataFrame(indicator_data)
        
        # Create query engine and execute query
        engine = PandasQueryEngine(df=df)
        response = engine.query(query)
        return str(response)

    def validate_indicator_value(self, indicator_id: str, value: float) -> dict:
        """Validate if a value is within the indicator's defined range"""
        try:
            indicator = Indicator.objects.get(id=indicator_id)
            is_valid = indicator.validate_value(value)
            return {
                'indicator': indicator.name,
                'value': value,
                'is_valid': is_valid,
                'min_value': indicator.min_value,
                'max_value': indicator.max_value
            }
        except Indicator.DoesNotExist:
            return {'error': f'Indicator {indicator_id} not found'}