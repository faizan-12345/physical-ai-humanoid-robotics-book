---
id: 001
title: Architectural Plan for Humanoid Robotics Book
stage: plan
date: 2025-12-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-physical-ai-robotics-book
branch: 001-physical-ai-robotics-book
user: pc
command: /sp.plan
labels: ["architecture", "planning", "rag"]
links:
  spec: C:\Users\pc\HUMANOID-ROBOTICS-BOOK\specs\001-physical-ai-robotics-book\spec.md
  ticket: null
  adr: null
  pr: null
files:
 - C:\Users\pc\HUMANOID-ROBOTICS-BOOK\specs\001-physical-ai-robotics-book\plan.md
 - C:\Users\pc\HUMANOID-ROBOTICS-BOOK\specs\001-physical-ai-robotics-book\research.md
 - C:\Users\pc\HUMANOID-ROBOTICS-BOOK\specs\001-physical-ai-robotics-book\data-model.md
 - C:\Users\pc\HUMANOID-ROBOTICS-BOOK\specs\001-physical-ai-robotics-book\contracts\rag_api_openapi.yaml
 - C:\Users\pc\HUMANOID-ROBOTICS-BOOK\specs\001-physical-ai-robotics-book\quickstart.md
tests:
 - Not applicable for planning phase
---

## Prompt

```text
Create:
- Full technical architecture sketch for the entire system:
    - Book architecture (Docusaurus structure, module → chapter → section hierarchy)
    - RAG architecture (FastAPI backend, Qdrant Cloud, Neon Serverless Postgres, OpenAI Agents/ChatKit SDK)
    - Build and deployment pipeline architecture (GitHub Pages + repo structure)
- Section structure for all 4 modules + capstone:
    - Module 1: ROS 2 fundamentals
    - Module 2: Digital Twin development (Gazebo + Unity)
    - Module 3: NVIDIA Isaac fundamentals
    - Module 4: Vision-Language-Action systems
    - Capstone: Humanoid robot simulation with conversational AI control
- Research approach:
    - Research-concurrent approach (perform research *while* writing chapters, not prior)
    - Use official docs for ROS 2, Gazebo, Unity, Isaac Sim, OpenAI, Whisper, Qdrant, Neon, GitHub Pages
    - Verify correctness of code samples, diagrams, workflows
- Quality validation plan:
    - All book sections must pass factual validation against official sources
    - All code examples must run and be tested
    - All RAG chatbot answers must be verifiable via book content
    - UI/UX validation of the embedded chatbot within Docusaurus
    - Deployment verification (GitHub Pages + RAG API hosted)
    - Must meet success criteria defined in constitution and specification

Decisions needing documentation:
- Book tooling:
    - Docusaurus vs alternatives → choose Docusaurus (required by hackathon)
- Deployment options:
    - GitHub Pages vs Netlify vs Vercel → choose GitHub Pages (required)
- Database for RAG:
    - Qdrant Cloud vs Pinecone vs Weaviate → choose Qdrant (free tier required)
- Backend stack:
    - FastAPI vs Node.js → choose FastAPI (required)
- Model usage:
    - OpenAI Agents/ChatKit vs manually-coded GPT calls
- Embedding model choice:
    - OpenAI vs Voyage vs HuggingFace → choose OpenAI embeddings for compatibility
- Document chunking strategy:
    - By section, by paragraph, or hybrid → choose hybrid (section-level + paragraph-level)
- User-selected text RAG method:
    - Direct context override vs dynamic embedding → choose dynamic embedding of user-selected text at runtime
- Deployment options for backend:
    - Render, Railway, Fly.io, local → choose Render (free tier recommended)

Testing strategy:
- Validate that:
    - All book content builds without errors in Docusaurus
    - Book deploys correctly on GitHub Pages (check routing, links, MDX blocks)
    - RAG backend:
        - Successfully stores embeddings in Qdrant
        - Successfully retrieves context based on queries
        - Successfully handles user-selected text
        - Correctly stores logs and user interactions in Neon Serverless Postgres
    - Chatbot:
        - Integrated and visible across the entire Docusaurus site
        - Can answer questions strictly from the book
        - Can answer questions only from user-selected text
    - API tests:
        - POST /embed
        - POST /query
        - POST /selected-text-query
        - ChatKit/Agent endpoints
- Acceptance criteria:
    - Content accuracy validated against official tools
    - Working chatbot embedded in book
    - Demonstrates a complete end-to-end RAG workflow

Technical details:
- Use research-concurrent approach (research while writing, not upfront)
- Follow writing clarity & accuracy rules defined in the Constitution
- Organize project by phases:

Phases:
1. **Research Phase**
    - Gather official documentation references
    - Confirm book’s 4-module structure
    - Collect example code for ROS2, Gazebo, Unity, Isaac, Whisper, and ChatKit
2. **Foundation Phase**
    - Create Docusaurus project
    - Create directory structure for modules
    - Create backend FastAPI project
    - Connect Qdrant + Neon
3. **Analysis Phase**
    - Break down content into chapters & pages
    - Analyze embedding strategy
    - Design chatbot UI/UX
    - Create diagrams & flowcharts
4. **Synthesis Phase**
    - Write book content module-by-module
    - Build RAG backend
    - Integrate chatbot into D
```

## Response snapshot

The planning phase for the "Physical AI & Humanoid Robotics Technical Book Creation" feature has been completed. This involved updating the `plan.md` with technical context and constitution checks, generating `research.md` for performance goals of RAG systems and Docusaurus sites, defining the `data-model.md` for key entities, creating the `contracts/rag_api_openapi.yaml` for the RAG backend API, and establishing a `quickstart.md` guide. The project structure has been defined as a `book-frontend` (Docusaurus) and `rag-backend` (FastAPI) application. The agent context was also updated to reflect the new technologies.

## Outcome

- ✅ Impact: The architectural plan for the entire system, including book architecture, RAG architecture, and deployment pipeline, has been established. Section structures for all modules and capstone are outlined. Research and quality validation approaches are defined. Key technical decisions are documented.
- 🧪 Tests: Not applicable for planning phase.
- 📁 Files: `plan.md`, `research.md`, `data-model.md`, `contracts/rag_api_openapi.yaml`, `quickstart.md`
- 🔁 Next prompts: Proceed to task generation based on this plan.
- 🧠 Reflection: The planning process successfully broke down a complex feature into manageable phases and defined the necessary artifacts.

## Evaluation notes (flywheel)

- Failure modes observed: The `create-phr.ps1` script failed to execute, requiring manual PHR generation.
- Graders run and results (PASS/FAIL): Not applicable.
- Prompt variant (if applicable): Not applicable.
- Next experiment (smallest change to try): Investigate `create-phr.ps1` execution issues.
