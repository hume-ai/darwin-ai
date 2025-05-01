Okay, let's craft a Product Requirements Document (PRD) for Version 1 (V1) of your "Second Brain" application. This PRD focuses on delivering the core value proposition in an achievable scope, laying the foundation for your larger vision, while keeping technical feasibility and your non-technical perspective in mind.

Product Requirements Document: "darwin-ai" V1 (Code Name)

1. Introduction

darwin-ai aims to be a next-generation personal knowledge management system (PKM), acting as a user's "Second Brain." Unlike traditional note-taking apps, darwin-ai integrates AI deeply to help users not only store but also interact with, connect, and understand their own information across different facets of their lives. V1 focuses on establishing the core foundation: capturing diverse information, organizing it intuitively, enabling AI-powered conversational retrieval with granular access control, and visualizing connections.

2. Goals for V1

Core Capture: Enable users to easily capture essential forms of personal information (text, links, images) into a structured system.

Intuitive Organization: Allow users to compartmentalize information using familiar concepts like folders (representing "Personas" or contexts) and tags.

AI-Powered Retrieval: Provide an AI chat interface allowing users to query their own stored information conversationally.

Granular Context Control: Empower users to select which compartments (folders) the AI chat can access when answering questions, ensuring privacy and focus.

Connection Visualization: Offer a basic interactive knowledge graph to help users visualize relationships between their notes.

Foundation for Growth: Build a stable, usable application with a clean UI that can be expanded upon in future versions (towards multi-modal, agents, MCP, etc.).

User Delight: Provide a smooth, aesthetically pleasing (inspired by "Severance" theme, usability of Obsidian) user experience.

3. Target Audience (V1)

Individuals using or seeking digital PKM tools (like Obsidian, Roam, Notion) who desire more integrated AI capabilities.

Professionals, students, writers, creators, and lifelong learners looking to better manage and leverage their personal knowledge base.

Users comfortable with digital tools who feel overwhelmed by scattered information across different apps and platforms.

4. Key Features (V1)

Feature ID	Feature Name	Description	Priority	Notes
CORE-01	User Accounts	Secure user signup, login, and basic profile management.	Must Have	Use a reliable auth provider (e.g., Supabase Auth, NextAuth).
CORE-02	Note Creation/Editing	A clean editor to create/edit notes. Supports: <br> - Rich Text (Markdown preferred for simplicity/exportability) <br> - Adding Hyperlinks <br> - Uploading Images (stored securely) <br> - Assigning Note to one Folder <br> - Adding multiple Tags <br> - Automatic timestamp (created/updated), manually editable.	Must Have	Focus on a simple, reliable editor. Image storage needs cost consideration (e.g., Cloudflare R2, Supabase Storage).
ORG-01	Folder Management	Create, rename, delete Folders. Folders represent the primary compartments ("Personas"). A note belongs to exactly one Folder.	Must Have	Simple hierarchy (no nested folders in V1).
ORG-02	Tag Management	Create tags, assign tags to notes, view all notes associated with a specific tag.	Must Have	Tags provide cross-folder linking mechanism.
AI-01	AI Chat Interface	A dedicated chat panel/screen where users can converse with an AI.	Must Have	
AI-02	Context Selection	Crucial: Before querying, the user MUST be able to easily select/deselect which Folders the AI chat should use as context for the current conversation or query. The AI response should only be based on information within the selected Folders.	Must Have	This is the core of compartmentalized access. UI needs to be very clear.
AI-03	RAG Implementation	Backend implements Retrieval-Augmented Generation (RAG). When a user asks a question, the system: <br> 1. Searches relevant notes within the selected Folders (using embeddings/vector search). <br> 2. Provides relevant chunks to an LLM (e.g., OpenAI API, Anthropic API - user likely needs own API key for V1). <br> 3. LLM generates an answer based only on the provided context.	Must Have	Requires setting up vector embeddings (on note creation/update) and vector search.
AI-04	Chat History	Store and display the history of conversations within the AI Chat interface.	Must Have	Store user prompts and AI responses.
VIS-01	Knowledge Graph View	A visual representation of notes as nodes. Edges connect notes based on: <br> 1. Direct [[wiki-links]] within note text (if editor supports). <br> 2. Shared Tags (optional view). <br> Graph should be interactive (zoom, pan, click node to navigate to the note).	High	Leverage libraries like react-flow. Keep it simple initially. Inspired by Obsidian graph.
UIX-01	Dashboard/Navigation	A central view showing folders, notes list, access to chat, and graph view. Clear navigation between sections.	Must Have	Prioritize clarity and ease of use.
UIX-02	Responsive Design	Application must be usable and look good on desktop and mobile devices.	Must Have	Use Tailwind CSS effectively.
UIX-03	Theming	Apply a clean, potentially dark-themed aesthetic inspired by "Severance" / modern minimalist design. Use Shadcn/ui components.	Must Have	Consistency and polish are key.

5. User Flow (V1 - Simplified)

Signup/Login: User creates an account or logs in.

Dashboard: User lands on the main dashboard. Sees options to create notes/folders, view existing ones, access chat, access graph.

Create Folder: User creates a new Folder (e.g., "Work Project," "Personal Journal," "Book Ideas").

Create Note: User clicks "Add Note."

Selects the Folder for the note (e.g., "Book Ideas").

Adds a title ("Chapter 1 Outline").

Writes content (text, links).

Uploads an image (e.g., cover inspiration).

Adds tags (#fiction, #character-dev).

Saves the note.

View Graph: User navigates to the Knowledge Graph view. Sees nodes for notes, potentially linked by tags. Can click a node to open the note.

AI Chat Interaction: User opens the AI Chat interface.

Selects Context: User explicitly chooses which Folders to include (e.g., ticks checkboxes for "Book Ideas" and "Personal Journal").

Asks Question: User types: "What were the main character ideas I had last week?"

System Processes: Backend finds relevant notes only within "Book Ideas" and "Personal Journal," sends context to LLM.

Receives Answer: AI responds based only on the content within those selected folders.

Manage: User can rename folders, edit/delete notes, manage tags.

6. Technical Stack & Considerations (V1)

Frontend: React (Next.js preferred for structure/routing), TypeScript, Tailwind CSS, Shadcn/ui

Backend: Node.js/TypeScript (or Python/FastAPI). Needs API endpoints for CRUD on notes/folders/tags, RAG pipeline, chat history.

Database:

Primary/Metadata: PostgreSQL (via Supabase, Neon, or self-hosted). Stores user data, note metadata, folder structure, tags, text content (or pointers to text files).

Vector Storage: A vector database extension/service integrated with Postgres (e.g., pgvector) or a dedicated vector DB (e.g., Pinecone, Weaviate - consider free tier limits). Needed for RAG.

File Storage: Cloudflare R2, AWS S3, Google Cloud Storage, Supabase Storage (for images). Consider costs.

LLM Integration: API integration with OpenAI, Anthropic, or similar. User likely provides their own API key in V1 to manage costs/usage.

Deployment: Vercel/Netlify (Frontend), Render/Fly.io/Supabase Functions (Backend), Managed DB services. Aim for low-cost/free tiers initially.

Knowledge Graph Lib: react-flow or similar.

7. Non-Functional Requirements (V1)

Usability: Interface must be intuitive and require minimal learning curve for core actions.

Performance: Note loading, search, and basic chat interactions should feel responsive. RAG performance depends on indexing and LLM speed.

Security: Secure authentication, proper authorization (user can only access their own data), protection against common web vulnerabilities (OWASP Top 10). Image storage access control. No data sharing between users in V1.

Scalability: While V1 focuses on individual users, database schema and backend design should allow for future scaling (e.g., efficient indexing). Acknowledge free tier limitations.

Maintainability: Adhere to code quality principles (as outlined in your persona doc: small components, TypeScript, tests for critical logic, documentation).

8. Out of Scope for V1

Enterprise Features: No shared folders, team accounts, or specific enterprise roles (PM/Engineer agents).

Advanced Agent Interaction: No internal agent communication (A2A). The only "agent" is the main AI chat.

MCP (Model Context Protocol): No external exposure of context via a custom protocol or dedicated API endpoint for external LLMs yet. Focus on the internal AI chat first.

Advanced Multi-modal: No video/audio input, processing, or analysis. Image analysis beyond basic storage is out of scope.

Deep AI Correlation/Reasoning: AI insights limited to RAG retrieval based on selected folders. No complex cross-modal or semantic reasoning beyond vector similarity.

Automated Integrations: No connections to Slack, Jira, Notion, Google Docs, etc. All input is manual.

Past/Present/Future Sections: Organization relies solely on user-created Folders and Tags.

Offline Mode: Assumes online connectivity.

Advanced Graph Analysis: Graph is for visualization, not complex querying or AI-driven connection finding (beyond explicit links/tags).

9. Success Metrics (V1)

Activation Rate: % of signups who create >= 5 notes and >= 2 folders within the first week.

Retention Rate: Weekly/Monthly Active Users.

Feature Engagement: Frequency of AI chat usage, number of folders selected per chat session, graph view usage.

Qualitative Feedback: User surveys/interviews focusing on ease of use, usefulness of AI chat, and value of compartmentalization.

Performance: Average chat response time, page load speeds.

10. Future Considerations (Post-V1)

Implement the "Secure Context API" (your MCP idea) for external LLM integration.

Introduce more advanced multi-modal support (audio transcription, deeper image analysis).

Develop internal "Agent" capabilities based on folders/personas.

Explore more sophisticated AI for cross-compartment correlation.

Build automated integrations with third-party services.

Develop Enterprise features for team collaboration.

This V1 PRD provides a solid, achievable starting point that delivers core value aligned with your vision. It prioritizes the unique aspects (compartmentalized AI chat, visualization) while deferring significant complexity.