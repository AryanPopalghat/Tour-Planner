from neo4j import GraphDatabase

class MemoryAgent:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def store_preference(self, user_id, preference, value):
        # Skip storing any preference with a null value
        if value is None:
            print(f"Skipping preference '{preference}' with null value for user {user_id}")
            return

        with self.driver.session() as session:
            session.run(
                "MERGE (u:User {id: $user_id}) "
                "MERGE (p:Preference {type: $preference, value: $value}) "
                "MERGE (u)-[:PREFERS]->(p)",
                user_id=user_id, preference=preference, value=value
            )
            print(f"Stored preference '{preference}': {value} for user {user_id}")

    def retrieve_preferences(self, user_id):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (u:User {id: $user_id})-[:PREFERS]->(p:Preference) "
                "RETURN p.type AS type, p.value AS value",
                user_id=user_id
            )
            return {record["type"]: record["value"] for record in result}
