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

## Claude Desktop / Cursor MCP Configuration

This API is compatible with Claude Desktop and Cursor through the Model Control Panel (MCP) integration. The MCP allows AI assistants to interact directly with the API.

### Setup

To configure Claude Desktop or Cursor to work with this API, add the following configuration:

```json
{
    "mcpServers": {
      "reminders": {
        "command": "npx",
        "args": [
          "-y",
          "mcp-remote@latest",
          "http://localhost:8000/mcp",
          "--allow-http",
          "--transport sse-only"
        ]
      }
    }
}
```

This configuration:
- Names the MCP service "reminders"
- Uses `npx` to run the `mcp-remote` package
- Connects to the API at `http://localhost:8000/mcp`
- Allows HTTP connections (since we're using localhost)
- Specifies the SSE (Server-Sent Events) transport method

After adding this configuration, restart Claude Desktop to apply the changes and enable the integration.

### Testing with LLM

Here's an example conversation with an LLM using the MCP integration:

**User**: what can i do with reminders?

**LLM**:
I'd be happy to help you understand what you can do with the reminders system! Based on the available API functions, here are the main things you can do with reminders:

- Create new reminders with titles, optional descriptions, and optional due dates
- View all your existing reminders
- Get details about a specific reminder
- Update existing reminders
- Delete reminders you no longer need

The reminders system lets you keep track of tasks or events with basic information. Each reminder has a title (required), and can optionally include a more detailed description and a due date.

Would you like me to show you an example of how to create or manage reminders? Or is there something specific about reminders you'd like to know more about?

**User**: list all reminders avaiable

**LLM**:
I'll help you list all the available reminders. Let me retrieve that information for you.

```
read_reminders_reminders__get
```

It looks like there are currently no reminders in the system. The list is empty.

Would you like me to help you create a new reminder? I can show you how to add one with a title, description, and optional due date.

**User**: ok let's create 3:
first record video of mcp on youtube
second edit it
third publish it

**LLM**:
I'll help you create those three reminders. Let me create them one by one for you.

```
create_reminder_reminders__post
```

```
create_reminder_reminders__post
```

```
create_reminder_reminders__post
```

Great! I've successfully created all three reminders for your YouTube video project:

1. "Record video of MCP on YouTube" (ID: 2c907900-f610-4fa8-9004-a398bc36dbef)
2. "Edit MCP video" (ID: aeef49f9-8ccb-44c3-b03d-3050a431fd31)
3. "Publish MCP video" (ID: 406436fa-52a1-45e9-bec9-dac17a32e1d8)

These reminders are now in the system and organized in the proper sequence. Would you like to add due dates to any of them, view all your reminders again, or is there anything else you'd like to do with these reminders?

**User**: ok list now reminders that exist

**LLM**:
I'll retrieve the list of all existing reminders for you.

```
read_reminders_reminders__get
Request

{}
Response

[
  {
    "title": "Record video of MCP on YouTube",
    "description": "First step: Create and record the MCP video for YouTube",
    "due_date": null,
    "id": "2c907900-f610-4fa8-9004-a398bc36dbef",
    "created_at": "2025-05-04T18:40:57.223000"
  },
  {
    "title": "Edit MCP video",
    "description": "Second step: Edit the recorded MCP video",
    "due_date": null,
    "id": "aeef49f9-8ccb-44c3-b03d-3050a431fd31",
    "created_at": "2025-05-04T18:41:01.161000"
  },
  {
    "title": "Publish MCP video",
    "description": "Third step: Publish the edited MCP video to YouTube",
    "due_date": null,
    "id": "406436fa-52a1-45e9-bec9-dac17a32e1d8",
    "created_at": "2025-05-04T18:41:05.077000"
  }
]
```

Here are all your existing reminders:

1. **Record video of MCP on YouTube**
   - Description: First step: Create and record the MCP video for YouTube
   - Created: May 4, 2025
   - ID: 2c907900-f610-4fa8-9004-a398bc36dbef

2. **Edit MCP video**
   - Description: Second step: Edit the recorded MCP video
   - Created: May 4, 2025
   - ID: aeef49f9-8ccb-44c3-b03d-3050a431fd31

3. **Publish MCP video**
   - Description: Third step: Publish the edited MCP video to YouTube
   - Created: May 4, 2025
   - ID: 406436fa-52a1-45e9-bec9-dac17a32e1d8

All three reminders for your YouTube video project are now in the system in the proper sequence. None of them currently have due dates assigned. 