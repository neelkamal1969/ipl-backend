# IPL Backend API

A production-ready backend service for an IPL (Indian Premier League) analytics and match management dashboard.  
This backend exposes RESTful APIs to serve match data, team statistics, and aggregated insights, and is designed with clean architecture, scalability, and maintainability in mind.

## Table of Contents

1. [Project Overview](#1-project-overview)  
2. [Tech Stack](#2-tech-stack)  
3. [Architecture Overview](#3-architecture-overview)  
4. [API Design](#4-api-design)  
5. [Database Design](#5-database-design)  
6. [OpenAPI Documentation](#6-openapi-documentation)  
7. [Environment Configuration](#7-environment-configuration)  
8. [Local Setup Instructions](#8-local-setup-instructions)  
9. [Deployment Details](#9-deployment-details)  
10. [Project Structure](#10-project-structure)  
11. [Key Design Decisions](#11-key-design-decisions)  
12. [Limitations and Scope](#12-limitations-and-scope)  
13. [Future Improvements](#13-future-improvements)  

## 1. Project Overview

The IPL Backend API is responsible for:
- Serving IPL match and team data
- Providing statistical insights such as wins by team and matches by venue
- Handling pagination and structured responses
- Acting as a decoupled backend for a React-based frontend application

The backend follows a **service-oriented design** and is intentionally separated from the frontend to allow independent scaling, testing, and deployment.

This project emphasizes robustness, with error handling for database connections, invalid requests, and edge cases in data aggregation. It supports high concurrency through asynchronous operations where applicable, making it suitable for production environments with moderate traffic.

## 2. Tech Stack

- **Language:** Python 3
- **Framework:** FastAPI (chosen for its high performance, async support, and auto-generated docs)
- **Database:** PostgreSQL (relational database for structured data integrity)
- **ORM:** SQLAlchemy (for abstracting database interactions and supporting complex queries)
- **API Documentation:** OpenAPI (Swagger) (integrated natively with FastAPI)
- **Server:** Uvicorn (ASGI server for running FastAPI apps efficiently)
- **Deployment Platform:** Render (for easy cloud hosting with managed databases)

Additional libraries include Pydantic for data validation and schemas, ensuring type safety and serialization.

## 3. Architecture Overview

The backend follows a layered architecture to promote separation of concerns and ease of maintenance:

- **Client (Frontend) → FastAPI Routers (API Layer)**: Handles incoming requests, validates inputs, and routes to appropriate services.
- **Service / Business Logic Layer**: Contains core logic for data processing, aggregations, and transformations.
- **SQLAlchemy ORM**: Abstracts database queries, ensuring portability and reducing SQL injection risks.
- **PostgreSQL Database**: Stores persistent data with relational constraints.

### Architectural Principles Used
- **Separation of Concerns**: Each layer focuses on a single responsibility (e.g., routers handle HTTP, services handle logic).
- **Stateless REST APIs**: No session state is maintained, enabling easy scaling.
- **Clear Distinction Between Routing, Schemas, and Database Models**: Schemas (Pydantic) validate API data, while models (SQLAlchemy) define database structures.
- **Environment-Agnostic Configuration**: Uses environment variables for flexibility across dev, staging, and prod.

This design allows for modular testing (unit tests for services, integration tests for APIs) and future extensions like microservices.

## 4. API Design

The API is RESTful, resource-oriented, and follows standard HTTP methods for predictability. All endpoints return JSON responses with consistent structures, including success indicators, data payloads, and error messages.

### Example Endpoints

| Method | Endpoint                  | Description                                      |
|--------|---------------------------|--------------------------------------------------|
| GET    | /health                   | Health check endpoint to verify server status    |
| GET    | /teams                    | Fetch all teams with their details               |
| GET    | /matches                  | Fetch matches with pagination support            |
| GET    | /stats/wins-by-team       | Aggregated statistics on wins per team           |
| GET    | /stats/matches-by-venue   | Venue-based match distribution and counts        |

### Pagination Example
- Endpoint: `/matches?page=1&limit=10`
- Query Parameters: `page` (integer, default 1), `limit` (integer, default 10, max 100 to prevent overload)
- Response Structure:
  ```json
  {
    "success": true,
    "data": [ /* array of match objects */ ],
    "total": 500,
    "page": 1,
    "limit": 10
  }
  ```

Error responses follow a standard format (e.g., 400 for bad requests, 500 for server errors) with descriptive messages.

## 5. Database Design

The database schema is optimized for read-heavy operations, with indexes on frequently queried fields like `match_date` and foreign keys.

### Core Tables

#### Teams
- `id` (Primary Key, Integer, Auto-increment)
- `name` (String, Unique, Not Null)
- `short_name` (String, Unique, Not Null)

#### Matches
- `id` (Primary Key, Integer, Auto-increment)
- `season` (Integer, Not Null)
- `venue` (String, Not Null)
- `team1_id` (Foreign Key to Teams.id, Not Null)
- `team2_id` (Foreign Key to Teams.id, Not Null)
- `winner_id` (Foreign Key to Teams.id, Nullable)
- `match_date` (Date, Not Null)

### Relationships
- One-to-Many: A team can participate in many matches (via `team1_id`, `team2_id`, `winner_id`).
- Aggregated Queries: Use SQLAlchemy's query expressions for joins and groupings (e.g., `GROUP BY team.name` for wins).

Data integrity is enforced via foreign key constraints and unique indexes.

## 6. OpenAPI Documentation

FastAPI automatically generates interactive API documentation, reducing the need for manual docs.

### Swagger UI
- Accessible at: `/docs`
- Features: Interactive endpoint testing, request/response examples, authentication simulation (if added later).

### ReDoc
- Accessible at: `/redoc`
- Features: Clean, readable schema views with search functionality.

These tools allow developers to explore APIs without running code, aiding integration and debugging.

## 7. Environment Configuration

The app uses environment variables for security and flexibility. Load them via a `.env` file in development.

Required Variables:
- `DATABASE_URL=postgresql://username:password@host:port/dbname`

Optional:
- `DEBUG=True` (for verbose logging in dev)

The configuration is loaded at startup, with validation to prevent runtime errors.

## 8. Local Setup Instructions

### Prerequisites
- Python 3.9+
- PostgreSQL (installed and running)
- pip (Python package manager)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/neelkamal1969/ipl-backend.git
   cd ipl-backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/macOS
   # Or on Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database:
   - Create a PostgreSQL database (e.g., via `psql` or pgAdmin).
   - Update `DATABASE_URL` in your `.env` file.

5. Run migrations or schema setup (if using Alembic, add here; currently, schemas are created on-the-fly via SQLAlchemy).

6. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

The server will be available at: http://localhost:8000

## 9. Deployment Details

The backend is deployed on Render for reliable hosting.

- **Live Backend URL**: https://ipl-backend-z0i3.onrender.com
- **Deployment Features**:
  - Managed PostgreSQL instance.
  - Environment variables for secure secret management.
  - Automatic build and deploy via GitHub integration.
  - Scaling options for increased traffic.

Monitor logs and metrics via Render's dashboard.

## 10. Project Structure

```
ipl-backend/
├── app/
│   ├── main.py          # Entry point for the FastAPI app
│   ├── database.py      # Database connection and session management
│   ├── models/          # SQLAlchemy database models
│   ├── schemas/         # Pydantic schemas for API validation
│   ├── routers/         # API endpoint definitions
│   ├── services/        # Business logic and query services
├── requirements.txt     # Dependency list
├── README.md            # This documentation
```

This structure ensures single-responsibility principle, making navigation intuitive.

## 11. Key Design Decisions

- **FastAPI**: Selected for superior performance (async), type hints, and built-in docs over alternatives like Flask.
- **PostgreSQL**: Chosen for ACID compliance and support for complex analytics queries.
- **SQLAlchemy ORM**: Abstracts SQL for maintainability, while allowing raw queries for optimization.
- **Stateless APIs**: Enables easy load balancing and containerization (e.g., Docker in future).

These choices balance speed, reliability, and developer experience.

## 12. Limitations and Scope

- **No Authentication/Authorization**: Omitted to focus on core functionality; suitable for public dashboards.
- **Dataset Scope**: Limited to essential IPL metrics; no real-time data ingestion.
- **No Caching**: Relies on database for all queries; fine for current scale but may need Redis for growth.

These are deliberate tradeoffs for simplicity and academic/industry evaluation focus.

## 13. Future Improvements

- Implement JWT-based authentication for secure access.
- Add Redis caching for frequent analytics queries.
- Integrate background jobs (e.g., Celery) for data updates.
- Write unit/integration tests using Pytest.
- Enhance CI/CD with GitHub Actions for automated testing/deployments.

## Author

Neelkamal Gupta  
Full Stack Developer

---
