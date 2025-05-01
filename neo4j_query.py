# neo4j_queries.py
from neo4j import GraphDatabase
import pandas as pd

# Neo4j connection parameters
NEO4J_URI = "bolt://localhost:7687"  # Change if your Neo4j instance is elsewhere
NEO4J_USER = "neo4j"                 # Default username
NEO4J_PASSWORD = "12345678"     # Change this to your Neo4j password

class Neo4jConnector:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def close(self):
        self.driver.close()
        
    def run_query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record for record in result]
    
    def query_to_dataframe(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            # Convert records to DataFrame
            records = []
            for record in result:
                records.append(dict(record))
            return pd.DataFrame(records)

# Main execution
if __name__ == "__main__":
    try:
        # Create connector
        connector = Neo4jConnector(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
        print("Connected to Neo4j successfully!")
        
        # Example queries
        print("\n----- Knowledge Graph Statistics -----")
        stats_query = """
        MATCH (n)
        RETURN 
            count(n) AS node_count,
            size(()-[]-()) AS relationship_count,
            size(labels(n)) AS label_count
        """
        stats_df = connector.query_to_dataframe(stats_query)
        print(stats_df)
        
        print("\n----- Node Count by Type -----")
        node_types_query = """
        MATCH (n)
        RETURN labels(n) AS node_type, count(*) AS count
        ORDER BY count DESC
        """
        node_types_df = connector.query_to_dataframe(node_types_query)
        print(node_types_df)
        
        print("\n----- Relationship Types -----")
        rel_types_query = """
        MATCH ()-[r]->()
        RETURN type(r) AS relationship_type, count(*) AS count
        ORDER BY count DESC
        """
        rel_types_df = connector.query_to_dataframe(rel_types_query)
        print(rel_types_df)
        
        print("\n----- Marie Curie's Relationships -----")
        marie_query = """
        MATCH (n:Entity {name: 'marie curie'})-[r]->(m)
        RETURN n.name AS subject, r.type AS relationship, m.name AS object
        UNION
        MATCH (n)-[r]->(m:Entity {name: 'marie curie'})
        RETURN n.name AS subject, r.type AS relationship, m.name AS object
        """
        marie_df = connector.query_to_dataframe(marie_query)
        print(marie_df)
        
        print("\n----- Most Connected Entities -----")
        connected_query = """
        MATCH (n)-[r]-()
        RETURN n.name AS entity, count(r) AS relationship_count
        ORDER BY relationship_count DESC
        LIMIT 10
        """
        connected_df = connector.query_to_dataframe(connected_query)
        print(connected_df)
        
        # Close the connection
        connector.close()
        print("\nConnection closed.")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Please make sure Neo4j is running and the connection details are correct.")