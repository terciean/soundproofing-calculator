# Frontend-Backend Interaction Mapping for Soundproofing Calculator

This document outlines the interaction points and data flow between the new frontend and the Python backend for the soundproofing calculator application.

## Overview

The frontend (likely a React application, based on the `BUILD_DIR` in `app.py`) communicates with the Python backend (Flask application) via a RESTful API. The backend provides various services, including soundproofing recommendations, solution calculations, cost estimations, and acoustic property lookups. Some static configuration data is also exposed directly to the frontend.

## Key Backend Modules and their Frontend Usage

### `app.py` (Main Backend Entry Point)

`app.py` is the core of the backend, exposing the following API endpoints that the frontend consumes:

*   **`/` and `/<path:path>` (Static File Serving):**
    *   **Purpose:** Serves the static files (HTML, CSS, JavaScript) of the React frontend application.
    *   **Frontend Interaction:** The frontend is served directly from this endpoint when the user navigates to the application's root URL.

*   **`/api/recommendations` (POST):**
    *   **Purpose:** Generates soundproofing recommendations based on user-provided noise and room profiles.
    *   **Backend Module:** `solutions.recommendation_engine`
    *   **Frontend Interaction:** The frontend sends a JSON payload containing `noise_profile` (type, intensity, direction, etc.) and `room_profile` (dimensions, room type, etc.) to receive tailored solution recommendations.

*   **`/api/calculate_solution` (POST):**
    *   **Purpose:** Calculates detailed information for a specific soundproofing solution.
    *   **Backend Module:** `solutions.solution_calculator`
    *   **Frontend Interaction:** The frontend sends `solution_name`, `dimensions`, and optionally `solution_type` to get detailed calculation results (e.g., material quantities, installation steps).

*   **`/api/calculate_costs` (POST):**
    *   **Purpose:** Estimates the costs for recommended soundproofing solutions.
    *   **Backend Module:** `solutions.cost_calculator`
    *   **Frontend Interaction:** The frontend sends `recommendations`, `dimensions`, and `blockages` to get a cost breakdown for the proposed solutions.

*   **`/api/acoustic_properties` (POST):**
    *   **Purpose:** Retrieves acoustic properties (STC rating, frequency response, transmission loss) for a given solution.
    *   **Backend Module:** `solutions.acoustic_calculator`
    *   **Frontend Interaction:** The frontend sends `solution_id` and `dimensions` to display detailed acoustic performance data for a selected solution.

*   **`/api/js_constants` (GET):**
    *   **Purpose:** Provides JavaScript constants (e.g., `SOLUTION_CATALOG`, `NOISE_PROFILES`) directly to the frontend.
    *   **Backend Module:** `solutions.config` (`get_js_constants` function)
    *   **Frontend Interaction:** The frontend fetches these constants on startup to populate dropdowns, display descriptions, and use in its internal logic without making separate API calls for each piece of static data.

*   **`/api/solution_catalog` (GET):**
    *   **Purpose:** Returns the full `SOLUTION_CATALOG` defined in `solutions.config`.
    *   **Backend Module:** `solutions.config`
    *   **Frontend Interaction:** Used to display all available soundproofing solutions, categorized by surface type and tier.

*   **`/api/noise_profiles` (GET):**
    *   **Purpose:** Returns all `NOISE_PROFILES` defined in `solutions.config`.
    *   **Backend Module:** `solutions.config`
    *   **Frontend Interaction:** Used to populate options for noise types in the frontend's input forms.

*   **`/api/solution_mappings` (GET):**
    *   **Purpose:** Returns `SOLUTION_MAPPINGS` defined in `solutions.config`.
    *   **Backend Module:** `solutions.config`
    *   **Frontend Interaction:** Used to guide the frontend in suggesting solutions based on noise type and performance tier.

*   **`/api/solution_descriptions` (GET):**
    *   **Purpose:** Returns `SOLUTION_DESCRIPTIONS` defined in `solutions.config`.
    *   **Backend Module:** `solutions.config`
    *   **Frontend Interaction:** Used to display brief descriptions of solutions in the frontend UI.

*   **`/api/all_solutions` (GET):**
    *   **Purpose:** Retrieves all available soundproofing solutions with their characteristics.
    *   **Backend Module:** `solutions.solutions` (`get_all_solutions` method)
    *   **Frontend Interaction:** Used to display a comprehensive list of all solutions, potentially for browsing or administrative purposes.

*   **`/api/solution_by_id/<string:solution_id>` (GET):**
    *   **Purpose:** Retrieves a single solution by its unique ID.
    *   **Backend Module:** `solutions.solutions` (`get_solution` method)
    *   **Frontend Interaction:** Used to fetch detailed information about a specific solution when selected by the user.

*   **`/api/implementation_details` (POST):**
    *   **Purpose:** Provides detailed implementation steps for a chosen solution.
    *   **Backend Module:** `solutions.solution_calculator` (`generate_implementation_details_detailed` function)
    *   **Frontend Interaction:** The frontend sends `solution_id`, `surface_type`, and `dimensions` to get step-by-step instructions for installing a solution.

### Other Backend Modules (Internal to Backend Logic)

The following modules are primarily used internally by the backend services and are not directly exposed as API endpoints to the frontend, though their logic underpins the data and calculations provided:

*   **`solutions/acoustic_calculator.py`:** Performs complex acoustic calculations. Used by `recommendation_engine` and exposed via `/api/acoustic_properties`.
*   **`solutions/base_calculator.py`:** Provides fundamental calculation logic for material quantities and costs. Used by various solution-specific calculators.
*   **`solutions/base_genieclip.py`:** A base class for GenieClip-based solutions (walls and ceilings), encapsulating common logic for these systems.
*   **`solutions/base_solution.py`:** The most fundamental base class for all soundproofing solutions, handling common functionalities like data loading and basic calculations.
*   **`solutions/base_sp15.py`:** A base class for SP15-enhanced solutions, providing specific logic for SP15 material calculations and acoustic properties.
*   **`solutions/blockage_calculator.py`:** Calculates areas and summaries of blockages (e.g., windows, doors). Used to adjust areas or costs based on blockages.
*   **`solutions/cache_manager.py`:** Manages in-memory caching for various backend operations to improve performance. Not directly exposed to the frontend.
*   **`solutions/config.py`:** Centralized configuration, directly providing static data to `app.py` for API exposure and internal use.
*   **`solutions/cost_calculator.py`:** Calculates costs. Exposed via `/api/calculate_costs`.
*   **`solutions/database.py`:** Handles all interactions with the MongoDB database.
*   **`solutions/logger.py`:** Configures and provides a centralized logging utility for the backend.
*   **`solutions/material_properties.py`:** Manages material characteristics and properties. Used by solution classes and acoustic calculations.
*   **`solutions/recommendation_engine.py`:** The core logic for generating recommendations. Exposed via `/api/recommendations`.
*   **`solutions/room.py`:** Defines the `Room` class, representing a physical room with dimensions, surface areas, blockages, and features. Used by the `recommendation_engine` to model the user's room.
*   **`solutions/solution_calculator.py`:** Performs detailed solution calculations and generates implementation details. Exposed via `/api/calculate_solution` and `/api/implementation_details`.
*   **`solutions/solution_mapping_new.py`:** Maps frontend solution names to backend calculator classes and database names. Used internally by `solution_calculator` and `recommendation_engine`.
*   **`solutions/solution_profiles.py`:** Defines and manages comprehensive profiles for each soundproofing solution. Used by `solutions.py` and `acoustic_calculator`.
*   **`solutions/solutions.py`:** Manages the retrieval and caching of all soundproofing solutions. Exposed via `/api/all_solutions` and `/api/solution_by_id`.
*   **`solutions/wall_solutions.py`:** Defines and consolidates various wall soundproofing solution classes (M20, GenieClip, Resilient Bar, Independent) and their SP15 variants. Used for initializing and managing wall solution instances.
*   **`solutions/walls/` (and its sub-modules like `M20Wall.py`, `GenieClipWall.py`, `resilientbarwall.py`, `Independentwall.py`):** These modules contain specific implementations of wall soundproofing solutions. They inherit from `base_wall.py` and define solution-specific calculation, acoustic property, and implementation detail methods. They are internal backend components used by `solution_calculator.py` and `recommendation_engine.py`.
*   **`solutions/ceilings/` (and its sub-modules like `genieclipceiling.py`, `independentceiling.py`, `lb3genieclipceiling.py`, `resilientbarceiling.py`):** These modules contain specific implementations of ceiling soundproofing solutions. They inherit from `base_solution.py` (directly or indirectly) and define solution-specific calculation, acoustic property, and implementation detail methods. They are internal backend components used by `solution_calculator.py` and `recommendation_engine.py`.

## Data Flow Summary

1.  **Frontend Initialization:** Fetches static configuration data (solution catalog, noise profiles, mappings, descriptions) from `/api/js_constants`, `/api/solution_catalog`, `/api/noise_profiles`, `/api/solution_mappings`, and `/api/solution_descriptions`.
2.  **User Input:** User provides noise and room details in the frontend.
3.  **Recommendation Request:** Frontend sends noise and room profiles to `/api/recommendations`.
4.  **Recommendation Display:** Frontend receives and displays recommendations.
5.  **Solution Details/Calculation Request:** If the user selects a specific solution, the frontend might request detailed calculations from `/api/calculate_solution` or implementation details from `/api/implementation_details`.
6.  **Cost Estimation:** Frontend sends recommendations and dimensions to `/api/calculate_costs` to get cost estimates.
7.  **Acoustic Properties Display:** Frontend can request acoustic properties for a solution from `/api/acoustic_properties` to show performance metrics.