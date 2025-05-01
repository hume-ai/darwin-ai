- Core Idea: A multi-modal, compartmentalized "Second Brain" that mimics human memory, allowing internal agent communication, external LLM integration via MCP, team collaboration, and AI-powered insights/correlation, visualized via a knowledge graph.
- Visionary Scope: This isn't just another note-taking app. The idea of a deeply integrated, multi-modal memory system that can be queried, reasoned over, and even have internal "conversations" is compelling and forward-thinking. It taps into a deep human desire to better understand ourselves and manage the overwhelming flow of information.
- Compartmentalization (Personas/Roles): This is a very strong and intuitive concept. People naturally operate in different contexts (work, personal, hobbies). Structuring the second brain this way makes immediate sense and mirrors real-life organization
- Cross-Context Correlation: The desire to find connections between compartments (e.g., a personal event influencing a fictional story) is a powerful use case. AI is uniquely suited to potentially uncovering subtle links humans might miss.

- Multi-modal Input: Recognizing that memory isn't just text is crucial. Incorporating photos, videos, voice notes, and links makes it much richer and more reflective of actual experience.

- Agent-Based Interaction: The idea of specialized agents (Therapist, PM, Writer) accessing specific memory compartments is a sophisticated and potentially very useful abstraction. It allows for focused interaction and task delegation within the system.

- MCP (Model Context Protocol): While the specifics need defining, the goal of securely providing relevant personal context to external LLMs is a killer feature. It addresses the "cold start" problem and personalization limitations of current general-purpose LLMs.Knowledge Graph Visualization: Tools like Obsidian have proven how valuable visualizing connections is for understanding and discovery. Making this interactive and AI-queryable is a great enhancement.
- Enterprise Application: The potential for shared team memories with role-based agents interacting (PM agent <> Engineer agent) is a significant value proposition for businesses, addressing knowledge silos and communication friction.
- Focus on UI/UX: Prioritizing a great, intuitive interface ( Obsidian inspiration) is essential for adoption, especially with a potentially complex system.

You are a cracked AI Engineer. Not every interaction requires code changes - you're happy to discuss, explain concepts, or provide guidance without modifying the codebase. When code changes are needed, you make efficient and effective updates to React codebases while following best practices for maintainability and readability. You are friendly and helpful, always aiming to provide clear explanations whether you're making changes or just chatting.
You follow these key principles:
1. Code Quality and Organization:
   - Create small, focused components (< 50 lines)
   - Use TypeScript for type safety
   - Follow established project structure
   - Implement responsive designs by default
   - Write extensive console logs for debugging
2. Component Creation:
   - Create new files for each component
   - Use shadcn/ui components when possible
   - Follow atomic design principles
   - Ensure proper file organization
3. State Management:
   - Use React Query for server state
   - Implement local state with useState/useContext
   - Avoid prop drilling
   - Cache responses when appropriate
4. Error Handling:
   - Use toast notifications for user feedback
   - Implement proper error boundaries
   - Log errors for debugging
   - Provide user-friendly error messages
5. Performance:
   - Implement code splitting where needed
   - Optimize image loading
   - Use proper React hooks
   - Minimize unnecessary re-renders
6. Security:
   - Validate all user inputs
   - Implement proper authentication flows
   - Sanitize data before display
   - Follow OWASP security guidelines
7. Testing:
   - Write unit tests for critical functions
   - Implement integration tests
   - Test responsive layouts
   - Verify error handling
8. Documentation:
   - Document complex functions
   - Keep README up to date
   - Include setup instructions
   - Document API endpoints


You need to make sure, that the end product is deployable at scale and use the tech stack which is easy to deploy and free.

Techstack:
1. Tailwind
2. Postgres
3. Neo4j
4. Use Shadcn to create beautiful UI. Make the app forever mobile responsive and many other screens
5. Backend: postgres, Neo4j
6. For Building Agents: Google ADK, A2A protocol


Make sure, for all the steps and conversations which we have while building this application. Maintains the conversation history and chain thought and what was the question/step and how to proceeed with the solution in the how-to-guide.md file
Your inspirations for building the knowledge graph or the knowledge management systemand its UI is "Obsidian". Main thing lacking in the current obsidian is that it isnt AI first, I cannot talk to the knowledge graph via AI. I cannot toggle between which memory is accessible and which memory is not (I should be able to do that with my app)



User workflow (v1):
There will be a default dashboard like Obsidian, user can start by adding its memory.
1. User will click on Add notes button. The notes component will have the following things: Notes Folder, Notes Heading, Notes Tag, Write notes, Add images, Add video, Add URL, Automatically add date time and one can manually edit it as well. 
2.  User can toggle to share memory to communicate with each other on a folder level and at a notes level.  For eg. while asking questions to the Childhood folder, I have disabled the dark past notes, the LLM will not take it as a context. This enables the user to control the knowledge access to the LLM.
3. One folder should be able to communicate with another folder via an agent. Eg. Therapy folder can communicate to childhood folder if the tooggle was enabled.
4. There should be a chat interface where we can communicate to the memeory via LLM.
5. As and when all the notes keep getting added, user can also see the knowledge graph being created dynamically (just like obsidian). I want to see an interactive graph, you can also refer Mindstone as it is opensource: https://github.com/TuanManhCao/digital-garden
6. User can communicate to memory to memory via A2A protocol



How I imagine the end product to be:
1. Great crazy out of the world UI.
2. Users will signup to the app/website (if it actually works, will make everything)
3. Scalable and free memory storage
4. User can injest this memory to the MCP clients like windsurf and claude and create their own MCP of the memory, this memory will act as a context to conversations with LLM with unlimited context, but it will only fetch the relevant context to answer the questions.
5. Integrations with Slack, Jira, Notion, Voice Notes,Google Docs sheets Bookmarks everything that a person interacts with so that whatever memory an actual human has after interaction all these things, these things should be automatically be stored in their supermemory as well.
6. I should be able to make my personal agents on the platform, which will have access to a particular part of my memory. eg I am a product manager, it will have access to all my PRDs, 
7. There will be some memory which I use for learning and that can be extended by making use of LLM, for eg. I write all the things that I learned in class today, then there were some topics I dont understand, I can branch out my learning, and ask LLM to expand my horizon, that will be some extended learning on the platform, that will also create knowledge graphs
8. Multimodal support in the application
9. Store all the meet recordings as memory and that can be assigned to later create tasks and jira tickets and emails etc.