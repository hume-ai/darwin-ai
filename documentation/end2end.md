1. Tech‑Stack Picks (we can tweak these if you like)
           • Frontend: Next.js with TypeScript (gives you React, SSR/SSG, easy API routes)
           • Backend: NestJS with TypeScript (opinionated, integrates nicely with GraphQL/REST)
           • Graph DB: Neo4j (property graph for your MemoryItems & edges)
           • Vector DB: Pinecone or Weaviate (for embeddings search)
           • Object Storage: AWS S3 (or MinIO locally for dev)
           • Auth: Auth0 or Firebase Auth (out‑of‑the‑box user management)
           • Monorepo: Yarn workspaces (keep “web” and “api” in one repo)
           • Containerization: Docker (for Neo4j, local dev services, and eventual deployment)
        2. Step 1: Scaffold Monorepo & Services
           a. Create root folder with a package.json configured for Yarn workspaces
           b. Scaffold “web” using `create-next-app --typescript`
           c. Scaffold “api” using `nest new --package-manager yarn --strict`
           d. Add Docker Compose for Neo4j, MinIO (or S3 emulator), and the vector DB (Pinecone can stay cloud‑hosted)
        3. Step 2: Implement Auth + User Onboarding
           • Hook up Auth0/Firebase in both web and api (secure routes, user context)
           • Build simple onboarding form (“Tell us about yourself”) and store profile in your DB
        4. Step 3: Data Model & Database Integration
           • Define the graph schema in Neo4j (User, Compartment, MemoryItem, Agent, Interaction, etc.)
           • Write a small NestJS module to connect to Neo4j and run Cypher migrations
           • Build REST/GraphQL endpoints to create/read Personas and MemoryItems
        5. Step 4: Memory Ingestion Pipeline
           • In NestJS: on MemoryItem creation → persist blob link, send text to embeddings API → index in Pinecone → create nodes & edges in Neo4j
           • Run as a background/queue worker (BullMQ or NestJS microservice)
        6. Step 5: Frontend Memory UI & Visualization
           • “Add Memory” form (text, photo upload, audio)
           • Timeline view per compartment
           • Graph view with Cytoscape/D3 using Neo4j sub‑graphs
        7. Step 6: Chat & MCP Integration
           • Chat component in Next.js connected via WebSockets to a NestJS “chat” gateway
           • MCP adapters for Claude & Windsurf: stream responses, show typing, persist each turn back into Neo4j
