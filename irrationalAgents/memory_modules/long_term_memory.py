from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance

class LongTermMemory: 
    def __init__(self, long_memory_path, qdrant_url='http://localhost:6333', collection_name='concept_nodes'): 
        self.id_to_node = dict()
        self.seq_event = []
        self.seq_thought = []
        self.seq_chat = []
        self.kw_to_event = dict()
        self.kw_to_thought = dict()
        self.kw_to_chat = dict()
        self.kw_strength_event = dict()
        self.kw_strength_thought = dict()
        self.embeddings = json.load(open(long_memory_path + "/embeddings.json"))
        
        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(url=qdrant_url)
        self.collection_name = collection_name
        
        # Create collection if it does not exist
        if self.collection_name not in self.qdrant_client.get_collections().collections:
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=768, distance=Distance.COSINE)  # Adjust vector size as per your embeddings
            )
            print(f"Qdrant Collection '{self.collection_name}' created.")
        else:
            print(f"Qdrant Collection '{self.collection_name}' already exists.")
        
        # Load existing nodes
        nodes_load = json.load(open(long_memory_path + "/nodes.json"))
        for count in range(len(nodes_load.keys())): 
            node_id = f"node_{str(count+1)}"
            node_details = nodes_load[node_id]
            
            node_count = node_details["node_count"]
            type_count = node_details["type_count"]
            node_type = node_details["type"]
            depth = node_details["depth"]
            
            created = datetime.datetime.strptime(node_details["created"], 
                                                '%Y-%m-%d %H:%M:%S')
            expiration = None
            if node_details["expiration"]: 
                expiration = datetime.datetime.strptime(node_details["expiration"],
                                                        '%Y-%m-%d %H:%M:%S')
            
            s = node_details["subject"]
            p = node_details["predicate"]
            o = node_details["object"]
            
            description = node_details["description"]
            embedding_key = node_details["embedding_key"]
            embedding_vector = self.embeddings.get(embedding_key)
            if embedding_vector is None:
                print(f"Warning: Embedding key {embedding_key} not found for node {node_id}. Skipping embedding upload.")
            else:
                embedding_pair = (embedding_key, embedding_vector)
            poignancy =node_details["poignancy"]
            keywords = set(node_details["keywords"])
            filling = node_details["filling"]
            
            if node_type == "event": 
                self.add_event(created, expiration, s, p, o, 
                           description, keywords, poignancy, embedding_pair, filling)
            elif node_type == "chat": 
                self.add_chat(created, expiration, s, p, o, 
                           description, keywords, poignancy, embedding_pair, filling)
            elif node_type == "thought": 
                self.add_thought(created, expiration, s, p, o, 
                           description, keywords, poignancy, embedding_pair, filling)
        
        kw_strength_load = json.load(open(long_memory_path + "/kw_strength.json"))
        if kw_strength_load.get("kw_strength_event"): 
            self.kw_strength_event = kw_strength_load["kw_strength_event"]
        if kw_strength_load.get("kw_strength_thought"): 
            self.kw_strength_thought = kw_strength_load["kw_strength_thought"]
