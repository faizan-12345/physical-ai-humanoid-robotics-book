# Data Model: Physical AI & Humanoid Robotics Technical Book Creation

## Key Entities

### Book Content
- **Description**: Represents the Docusaurus Markdown/MDX files, including text, code, diagrams, and examples.
- **Fields**:
    - `id`: Unique identifier for each content chunk (e.g., file path, section ID)
    - `text`: The actual content (e.g., Markdown text, code block)
    - `embedding`: Vector representation of the text, stored in Qdrant
    - `metadata`: Associated metadata (e.g., module, chapter, section title, URL, source file)

### RAG Chatbot Interactions
- **Description**: Represents user queries and chatbot responses, potentially stored in Neon Postgres for logging and analysis.
- **Fields**:
    - `interaction_id`: Unique identifier for each interaction
    - `user_query`: The raw text query from the user
    - `retrieved_context`: References to book content chunks used for grounding the response
    - `chatbot_response`: The generated response from the LLM
    - `timestamp`: When the interaction occurred
    - `user_feedback`: (Optional) User rating or feedback on the response

### Humanoid Robot Model
- **Description**: The virtual representation of the humanoid robot used in simulations and the Capstone project.
- **Fields**:
    - `model_id`: Unique identifier for the robot model
    - `urdf_path`: Path to the URDF file defining the robot's kinematics and visuals
    - `simulation_environment`: (e.g., Gazebo, Unity, Isaac Sim)
    - `capabilities`: (e.g., navigation, perception, manipulation)

## Relationships

- **Book Content** `has` **Embeddings** (stored in Qdrant)
- **User Queries** `retrieve` **Book Content** (via embeddings)
- **RAG Chatbot** `generates` **Responses** `based on` **Retrieved Content** and `logs` **Interactions** (in Neon Postgres)
- **Humanoid Robot Model** `is simulated in` **Simulation Environment**
