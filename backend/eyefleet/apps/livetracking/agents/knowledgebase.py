from llama_index import VectorStoreIndex, Document
from llama_index.node_parser import SimpleNodeParser
from typing import List
from ..models import Device, Indicator
from influxdb_client import InfluxDBClient
from django.conf import settings
import pandas as pd

class LivetrackingIndex:
    """Manages the LlamaIndex document store for telemetry data"""
    
    def __init__(self):
        self.parser = SimpleNodeParser()
        self.index = None
        self.influx_client = InfluxDBClient(
            url=settings.INFLUXDB_URL,
            token=settings.INFLUXDB_TOKEN,
            org=settings.INFLUXDB_ORG
        )
        
    def build_index(self):
        """Build the vector store index from telemetry data"""
        documents = self._get_documents()
        nodes = self.parser.get_nodes_from_documents(documents)
        self.index = VectorStoreIndex(nodes)
        
    def _get_documents(self) -> List[Document]:
        """Get all relevant telemetry documents"""
        documents = []
        query_api = self.influx_client.query_api()
        
        # Add device records
        devices = Device.objects.all()
        for device in devices:
            # Get recent telemetry summary for device
            query = f'''
            from(bucket: "{device.id.lower()}")
                |> range(start: -24h)
                |> group(columns: ["_measurement"])
                |> mean()
            '''
            try:
                result = query_api.query_data_frame(query)
                if not result.empty:
                    stats = result.to_dict('records')[0]
                else:
                    stats = {}
            except Exception:
                stats = {}
            
            doc = Document(
                text=f"""
                Device ID: {device.id}
                Name: {device.name}
                Status: {device.status}
                Vehicle: {device.assigned_vehicle}
                Location: {device.location}
                Battery Level: {device.battery_level}
                Recent Telemetry Stats: {stats}
                """
            )
            documents.append(doc)
        
        # Add indicator records
        indicators = Indicator.objects.all()
        for indicator in indicators:
            doc = Document(
                text=f"""
                Indicator ID: {indicator.id}
                Name: {indicator.name}
                Type: {indicator.data_type}
                Unit: {indicator.unit}
                Description: {indicator.description}
                Min Value: {indicator.min_value}
                Max Value: {indicator.max_value}
                Warning Threshold: {indicator.warning_threshold}
                Critical Threshold: {indicator.critical_threshold}
                """
            )
            documents.append(doc)
        
        return documents
    
    def query(self, query_text: str) -> str:
        """Query the telemetry knowledge base"""
        if not self.index:
            self.build_index()
        
        query_engine = self.index.as_query_engine()
        response = query_engine.query(query_text)
        return str(response)