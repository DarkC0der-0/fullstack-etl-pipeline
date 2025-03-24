# Full-Stack ETL Pipeline Project

## Overview

This project is a full-stack ETL (Extract, Transform, Load) pipeline designed to process and visualize data in real-time. It includes the following components:

- **Backend**: Built with FastAPI, it handles data extraction, transformation, and loading into a PostgreSQL database. It also uses Redis for caching and Pub/Sub.
- **Frontend**: Built with React, it provides a dynamic dashboard to visualize pipeline status and data.
- **Database**: PostgreSQL is used to store the processed data.
- **Caching**: Redis is used for caching intermediate results and Pub/Sub for real-time updates.
- **Monitoring**: Prometheus and Grafana are used for monitoring and visualizing metrics.

## Installation and Setup

### Prerequisites

- Docker and Docker Compose
- Node.js (for local frontend development)
- Python 3.9+ (for local backend development)

### Backend Setup

1. Navigate to the `backend` directory.
   ```bash
   cd backend
   ```

2. Install Python dependencies.
   ```bash
   pip install -r requirements.txt
   ```

3. Run the backend server.
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to the `frontend` directory.
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies.
   ```bash
   npm install
   ```

3. Run the frontend development server.
   ```bash
   npm start
   ```

### Docker Setup

1. Build and run the Docker containers.
   ```bash
   docker-compose up --build
   ```

This command will start the backend, frontend, PostgreSQL, Redis, Prometheus, and Grafana services.

## API Documentation

### Endpoints

#### Backend Endpoints

- **GET /api/pipeline-status**: Retrieve the current status of the pipeline.
- **GET /api/pipeline-logs**: Retrieve the logs of the pipeline.
- **GET /api/transformed-data**: Retrieve the transformed data.
- **GET /api/raw-data**: Retrieve the raw data.
- **POST /etl/api**: Trigger the ETL pipeline with a specified API URL.

### Request/Response Schemas

#### Example Request (POST /etl/api)

```json
{
  "api_url": "https://api.example.com/data"
}
```

#### Example Response (POST /etl/api)

```json
{
  "status": "success",
  "data": [...]
}
```

## Running Tests

### Backend Tests

1. Navigate to the `backend` directory.
   ```bash
   cd backend
   ```

2. Run the tests.
   ```bash
   pytest
   ```

### Frontend Tests

1. Navigate to the `frontend` directory.
   ```bash
   cd frontend
   ```

2. Run the tests.
   ```bash
   npm test
   ```

## Deployment Instructions

### Deploying to AWS ECS

1. Ensure your AWS credentials are configured.
2. Push the Docker images to Docker Hub.
3. Update the ECS service to use the new images.

### Continuous Integration and Deployment with GitHub Actions

A GitHub Actions workflow is configured to run tests, build Docker images, and deploy to AWS ECS on push to the `main` branch.

## Example Use Cases

1. **Real-Time Data Processing**: Extract data from various APIs, transform it, and load it into a database for real-time analysis.
2. **Data Visualization**: Use the frontend to visualize the processed data and monitor the pipeline status.

## Architecture Diagram

![Architecture Diagram](architecture_diagram.png)

This diagram shows the overall architecture of the ETL pipeline, including all components and their interactions.
