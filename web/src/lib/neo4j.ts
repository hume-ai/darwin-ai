import neo4j, { Driver, Session } from 'neo4j-driver';

/** Neo4j connection constants (override via environment) */
export const NEO4J_URI = process.env.NEO4J_URI || 'bolt://localhost:7687';
export const NEO4J_USER = process.env.NEO4J_USER || 'neo4j';
export const NEO4J_PASSWORD = process.env.NEO4J_PASSWORD || 'password';
export const NEO4J_DATABASE = process.env.NEO4J_DATABASE || 'neo4j';

/**
 * Connector for running Cypher queries against a Neo4j database.
 */
export class Neo4jConnector {
  private driver: Driver;
  constructor(
    uri: string = NEO4J_URI,
    user: string = NEO4J_USER,
    password: string = NEO4J_PASSWORD
  ) {
    this.driver = neo4j.driver(uri, neo4j.auth.basic(user, password));
  }
  /** Execute a Cypher query with parameters */
  async run_query(cypher: string, params: Record<string, any> = {}): Promise<any> {
    const session: Session = this.driver.session({ database: NEO4J_DATABASE });
    try {
      return await session.run(cypher, params);
    } finally {
      await session.close();
    }
  }
  /** Close the underlying driver connection */
  close(): Promise<void> {
    return this.driver.close();
  }
}
