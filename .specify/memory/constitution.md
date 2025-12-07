<!-- Sync Impact Report:
Version change: None -> 1.0.0
Modified principles: None
Added sections: Key Standards & Constraints, Success Criteria
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md: ✅ updated
- .specify/templates/spec-template.md: ✅ updated
- .specify/templates/tasks-template.md: ✅ updated
- .specify/templates/commands/*.md: ✅ updated
- README.md: ⚠ pending
- docs/quickstart.md: ⚠ pending
Follow-up TODOs: None
-->
# AI-Driven Technical Book Creation with Docusaurus + Integrated RAG Chatbot Constitution

## Core Principles

### Precision & Technical Accuracy
All modules and chapters must exhibit precision and technical accuracy. All explanations must be verifiable and reproducible with real code examples. All technical statements must be validated against official documentation (OpenAI, FastAPI, Docusaurus, Qdrant, Neon, GitHub Pages).

### Clarity & Accessibility
Content must be clear and accessible for beginners while remaining valuable for intermediate developers. Writing tone must be professional, instructor-level, with real-world relevance. Avoid unnecessary theoretical content—focus on actionable knowledge.

### Consistency
Maintain consistency in structure, terminology, and formatting across the entire book. This includes consistent file naming, folder structure, sidebar organization, and Markdown formatting.

### Spec-Driven AI-Assisted Development
AI-assisted writing must strictly follow spec-driven workflows: constitution → specs → plans → tasks → implementation. The entire book must be producible through Spec-Kit Plus. The entire creation process must follow the Spec-Kit Plus workflow precisely.

### Practical Applicability
Content must be practically applicable, actionable, and implementation-ready. Example code must be functional, minimal, and tested. All modules, chapters, and examples must be build-tested.

### Open Source & Free Tier First
No proprietary or paid APIs unless required; prefer free-tier services (Qdrant Cloud Free Tier, Neon Free Tier).

## Key Standards & Constraints

- Book format must follow Docusaurus structure (modules → chapters → pages).
- Version control: all deliverables prepared for GitHub Pages deployment.
- Must include explicit instructions for:
    - Docusaurus setup & GitHub Pages deployment
    - RAG chatbot architecture (OpenAI ChatKit/Agents, FastAPI, Neon, Qdrant)
    - Embed chatbot inside the published book
- All chapters must include diagrams, code blocks, and examples.

## Success Criteria

- Complete Docusaurus book generated, structured, and deployable without errors.
- GitHub Pages deployment successful and documented.
- Fully functional RAG chatbot integrated directly into the book.
- Chatbot must answer:
    - Questions about the whole book
    - Questions based on user-selected text only.

## Governance

Constitution supersedes all other practices. Amendments require documentation, approval, and a migration plan. All PRs/reviews must verify compliance. Complexity must be justified.

**Version**: 1.0.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-06
