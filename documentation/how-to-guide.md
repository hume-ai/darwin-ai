# How-to Guide for darwin-ai V1 Development
This document captures the step-by-step conversation history, design decisions, and development steps to build Version 1 (V1) of the darwin-ai "Second Brain" application.how 

## Step 1: Scaffold Frontend
User asked to "write me code to build this v1". We decided to scaffold a Next.js app in `web/` directory using:
```
npx create-next-app@latest web --typescript --tailwind --eslint --app --src-dir --use-npm --yes
```

This creates a Next.js App Router project with TypeScript, Tailwind CSS, and ESLint.

## Step 2: Add Tailwind Configuration
create-next-app did not generate a `tailwind.config` file. We manually added `web/tailwind.config.ts`:
```ts
import { defineConfig } from 'tailwindcss'
export default defineConfig({
  content: [
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: { extend: {} },
  plugins: [],
})
```

## Step 3: Update Global CSS
Replaced the default `@import "tailwindcss";` in `web/src/app/globals.css` with the Tailwind directives:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

## Step 4: Install Forms Plugin
- Install Tailwind Forms plugin for styling form elements:
  ```bash
  cd web
  npm install -D @tailwindcss/forms
  ```
- Update `tailwind.config.ts` to include the plugin:
  ```ts
  plugins: [
    require('@tailwindcss/forms'),
  ],
  ```

## Step 5: Create UI Primitives
We manually created core UI components in `web/src/components/ui`:
  - Button.tsx
  - Input.tsx
  - Textarea.tsx
  - Checkbox.tsx
  - Switch.tsx
  - ChatBubble.tsx

Each uses Tailwind classes for styling and can be imported from `@/components/ui`.

## Step 6: Scaffold API and React Query
- Installed React Query (`npm install @tanstack/react-query`) and created a `Providers` component to wrap the app in `layout.tsx`.
- Defined types in `src/types.ts` (Folder, Note) and an in-memory store in `src/lib/store.ts`.
- Added App Router API routes:
  - `src/app/api/folders/route.ts` (GET / POST / PUT)
  - `src/app/api/notes/route.ts` (GET / POST)

## Step 7: Hook Up Screens to API
- Updated `FolderList.tsx` to fetch and mutate folders via React Query.
- Created `NoteEditor.tsx` to POST notes via React Query.

## Step 8: Build Chat Interface
- Added a `ChatInterface.tsx` component under `src/components`:
  - Lets users toggle folder context, send messages, and displays stubbed AI responses via `ChatBubble`.

## Step 9: Add Chat and Graph Routes
- Create pages under `src/app/chat/page.tsx` and `src/app/graph/page.tsx`, importing the client components:
  ```tsx
  // chat/page.tsx
  export const dynamic = 'force-dynamic'
  import { ChatInterface } from '@/components/ChatInterface'
  export default function ChatPage() {
    return <ChatInterface />
  }
  ```
  ```tsx
  // graph/page.tsx
  export const dynamic = 'force-dynamic'
  import { KnowledgeGraph } from '@/components/KnowledgeGraph'
  export default function GraphPage() {
    return <KnowledgeGraph />
  }
  ```

## Step 10: Add Knowledge Graph View
- Installed `react-flow-renderer` with `npm install react-flow-renderer --legacy-peer-deps`.
- Created `src/components/KnowledgeGraph.tsx` using React Flow to visualize notes as nodes and shared-tags as edges.

## Step 11: Responsive Layout and Navigation
- Updated `src/app/layout.tsx` to include a top nav bar with links to Dashboard, Chat, and Graph.
- Updated `src/app/page.tsx` to use a responsive `flex flex-col md:flex-row h-screen` layout.
- Made `FolderList` responsive with `md:w-64 w-full md:border-r border-b` classes.

With these, the app now has:
1. Core note capture and organization (FolderList & NoteEditor)
2. AI chat interface (ChatInterface)
3. Interactive knowledge graph visualization (KnowledgeGraph)
4. Navigation among Dashboard, Chat, and Graph screens
5. In-memory demo backend via Next.js API routes

## Step 12: Build a Production Backend
We’re replacing the in-memory store with a dedicated Express server using Postgres and Neo4j.
1. Create a new `server/` directory with:
   - `package.json`, `tsconfig.json`, and `.env.example`
   - `src/db.ts` to connect to PostgreSQL (pg) and Neo4j (neo4j-driver), auto-creating tables
   - `src/routes/folders.ts` and `src/routes/notes.ts` (CRUD endpoints + Neo4j sync)
   - `src/index.ts` to assemble Express, CORS, JSON parsing, and mount routers
2. Run the backend in development:
   ```bash
   cd server
   npm install
   npm run dev
   ```
3. Configure your frontend to point to `http://localhost:4000` for data

This sets up a robust, scalable backend foundation for persisting data and evolving the knowledge graph.

Next up: polish UI/UX, integrate real AI backends for chat, persist data in Postgres/Neo4j, and expand multimodal support.

## Next Steps
- Integrate a production-ready RAG pipeline (embeddings, vector DB, retrieval)
- Connect a real LLM (OpenAI/Anthropic) via secure context (MCP)
- Add user authentication/authorization (NextAuth/Supabase)
- Persist and serve media assets (images, audio) via cloud storage
- Deploy frontend (Vercel) and backend (Heroku/Fly.io/Serverless)
- Enhance UI/UX: dark mode, accessibility, polished animations
- Expand to multi-modal and agent-based interactions

