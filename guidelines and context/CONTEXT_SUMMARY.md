# Project Context Summary

This file provides a high-level mapping of the relationships and integration points between the frontend, backend, and documentation for the Soundproofing Calculator project. It is designed to help maintain a holistic understanding of the codebase as it evolves.

---

## Frontend (JavaScript)
- **UI & Core JS**: Handles user interface, form state, and core logic. Main files: `data-service.js`, `endpoint-service.js`, `form-handlers.js`, etc.
  - **Backend Integration**: API calls to backend endpoints for data and recommendations.
- **JS Services & Utils**: Centralized API data fetching, error handling, and utility functions. Main files: `data-service.js`, `endpoint-service.js`, `error-handler.js`, etc.
  - **Backend Integration**: Fetches noise profiles, solution catalogs, and recommendations from backend.
- **Recommendations & Workflow**: Manages recommendation logic and workflow. Main files: `recommendation-manager.js`, `soundproofing-manager.js`, `workflow-manager.js`.
  - **Backend Integration**: Fetches recommendations and costs from backend; syncs static/fallback data.
- **Modules & Testing Tools**: Contains modules for solution processing and endpoint testing. Main files: `solution-processor.js`, `endpoint-test.js`, `endpoint-tester.js`.
  - **Backend Integration**: Fetches solution/material data and tests backend endpoints.

---

## Backend (Python)
- **Database Layer**:
  - `db_init.py`: Initializes MongoDB connections with retry logic and Flask integration.
  - `database.py`: Manages MongoDB data access, caching, and error handling. Provides functions like `get_solution_data()`, `get_solution()`, etc.
- **Recommendation Engine**:
  - `recommendation_engine.py`: Core logic for generating recommendations based on noise and room profiles.
- **Service Architecture**:
  - Layered architecture with DataService and EndpointService (mirrored in frontend for consistency).
  - Centralized error handling, caching, and retry logic.
- **Testing**:
  - `testmongo.py`, `test_db_connection.py`, `tests/test_recommendation_engine.py`: Test MongoDB connectivity, data integrity, and recommendation logic.

---

## Integration Points
- **API Endpoints**: Frontend services (`endpoint-service.js`, `data-service.js`) communicate with backend endpoints to fetch recommendations, solution data, and costs.
- **Database**: Backend uses MongoDB for storing and retrieving solution data, with caching and error resilience.
- **Recommendation Flow**: User input from frontend forms is sent to backend, processed by the recommendation engine, and results are returned for display.
- **Testing & Validation**: Both frontend and backend include modules for testing API endpoints and recommendation logic.

---

## Documentation Chunks
- **CHUNK_MAPPING_SUMMARY.md**: Maps chunk files to JavaScript and backend logic.
- **chunk 1 backend and misk.txt**: Summarizes backend tests and emergency frontend fixes.
- **chunk 1 database and utils.txt**: Details database and utility modules for floor, wall, and ceiling solutions.
- **chunk 1 database.txt**: Describes database initialization and access logic.
- **chunk 1 service architecture.txt**: Explains the layered service architecture and its benefits.

---

## Maintenance Notes
- Update this file as new integration points, modules, or architectural changes are introduced.
- Use this summary to onboard new developers and maintain cross-component understanding.