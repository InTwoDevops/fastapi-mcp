# Reminders API

A simple FastAPI application with basic CRUD operations for reminders, using MongoDB as the database.

## Features

- Create, read, update, and delete reminders
- Built with FastAPI (Pydantic 2) and MongoDB
- Containerized with Docker and Docker Compose
- Interactive API documentation with Swagger UI and ReDoc

## Prerequisites

- Docker and Docker Compose

## Running the Application

1. Clone this repository
2. Run the application with Docker Compose:

```bash
docker compose up
```

3. Access the application:
   - API root: [http://localhost:8000/](http://localhost:8000/)
   - Swagger UI documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
   - ReDoc documentation: [http://localhost:8000/redoc](http://localhost:8000/redoc)
   - OpenAPI JSON: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

## API Endpoints

| Endpoint | HTTP Method | Description |
|----------|-------------|-------------|
| `/` | GET | Get API information and available endpoints |
| `/reminders/` | POST | Create a new reminder |
| `/reminders/` | GET | Get all reminders |
| `/reminders/{reminder_id}` | GET | Get a specific reminder |
| `/reminders/{reminder_id}` | PUT | Update a reminder |
| `/reminders/{reminder_id}` | DELETE | Delete a reminder |

## Example Reminder

```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "due_date": "2023-12-31T12:00:00"
}
```

## Testing with curl

Here are some examples of how to use curl to test the API:

```bash
# Create a reminder
curl -X POST "http://localhost:8000/reminders/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread", "due_date": "2023-12-31T12:00:00"}'

# Get all reminders
curl -X GET "http://localhost:8000/reminders/"

# Get a specific reminder (replace {id} with the actual ID)
curl -X GET "http://localhost:8000/reminders/{id}"

# Update a reminder (replace {id} with the actual ID)
curl -X PUT "http://localhost:8000/reminders/{id}" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread, and cheese", "due_date": "2023-12-31T12:00:00"}'

# Delete a reminder (replace {id} with the actual ID)
curl -X DELETE "http://localhost:8000/reminders/{id}"
``` 