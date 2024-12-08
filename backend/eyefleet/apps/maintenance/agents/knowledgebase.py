from llama_index.core import VectorStoreIndex, Document
from llama_index.core.node_parser import SimpleNodeParser
from typing import List
from eyefleet.apps.maintenance.models.maintenance import Maintenance
from eyefleet.apps.maintenance.models.assets import Asset
from eyefleet.apps.maintenance.models.inspections import Inspection

class MaintenanceIndex:
    """Manages the LlamaIndex document store for maintenance data"""
    
    def __init__(self):
        self.parser = SimpleNodeParser()
        self.index = None
        
    def build_index(self):
        """Build the vector store index from maintenance data"""
        documents = self._get_documents()
        nodes = self.parser.get_nodes_from_documents(documents)
        self.index = VectorStoreIndex(nodes)
        
    def _get_documents(self) -> List[Document]:
        """Get all relevant maintenance documents"""
        documents = []
        
        # Add maintenance records
        maintenances = Maintenance.objects.all()
        for maintenance in maintenances:
            doc = Document(
                text=f"""
                Maintenance ID: {maintenance.id}
                Asset: {maintenance.ref_asset.registration_number}
                Type: {maintenance.type.id}
                Status: {maintenance.status.id}
                Priority: {maintenance.priority.id}
                Scheduled Date: {maintenance.scheduled_date}
                Notes: {maintenance.notes}
                """
            )
            documents.append(doc)
        
        # Add inspection records
        inspections = Inspection.objects.all()
        for inspection in inspections:
            doc = Document(
                text=f"""
                Inspection ID: {inspection.id}
                Asset: {inspection.ref_asset.registration_number}
                Type: {inspection.type.id}
                Status: {inspection.status.id}
                Findings: {inspection.findings}
                Comments: {inspection.comments}
                """
            )
            documents.append(doc)
        
        return documents
    
    def query(self, query_text: str) -> str:
        """Query the maintenance knowledge base"""
        if not self.index:
            self.build_index()
        
        query_engine = self.index.as_query_engine()
        response = query_engine.query(query_text)
        return str(response)