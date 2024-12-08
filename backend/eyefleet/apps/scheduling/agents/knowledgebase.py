from llama_index.core import VectorStoreIndex, Document
from llama_index.core.node_parser import SimpleNodeParser
from typing import List
from ..models.missions import Mission
from ..models.schedules import MissionSchedule

class SchedulingIndex:
    """Manages the LlamaIndex document store for scheduling data"""
    
    def __init__(self):
        self.parser = SimpleNodeParser()
        self.index = None
        
    def build_index(self):
        """Build the vector store index from scheduling data"""
        documents = self._get_documents()
        nodes = self.parser.get_nodes_from_documents(documents)
        self.index = VectorStoreIndex(nodes)
        
    def _get_documents(self) -> List[Document]:
        """Get all relevant scheduling documents"""
        documents = []
        
        # Add mission records
        missions = Mission.objects.all()
        for mission in missions:
            doc = Document(
                text=f"""
                Mission ID: {mission.id}
                Status: {mission.status}
                Priority: {mission.priority}
                Stops: {mission.stops}
                Description: {mission.description}
                Notes: {mission.notes}
                Total Weight: {mission.total_weight}
                Total Volume: {mission.total_volume}
                """
            )
            documents.append(doc)
        
        # Add schedule records
        schedules = MissionSchedule.objects.all()
        for schedule in schedules:
            doc = Document(
                text=f"""
                Schedule ID: {schedule.id}
                Mission: {schedule.reference_mission.id}
                Status: {schedule.status}
                Start Time: {schedule.start_time}
                End Time: {schedule.end_time}
                Deliveries: {schedule.deliveries}
                Notes: {schedule.notes}
                """
            )
            documents.append(doc)
        
        return documents
    
    def query(self, query_text: str) -> str:
        """Query the scheduling knowledge base"""
        if not self.index:
            self.build_index()
        
        query_engine = self.index.as_query_engine()
        response = query_engine.query(query_text)
        return str(response)