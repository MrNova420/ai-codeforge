# AI Dev Team - Example Projects

These examples demonstrate what the AI Dev Team can create.

## Examples

### 1. Fibonacci Calculator (`fibonacci_example.py`)
A Python module with both recursive and iterative implementations of Fibonacci sequence calculation.

**Features:**
- Recursive implementation
- Iterative implementation (more efficient)
- Performance comparison
- Full documentation

**Run:**
```bash
python3 fibonacci_example.py
```

### 2. REST API (`rest_api_example.py`)
A complete Flask REST API for user management with CRUD operations.

**Features:**
- Full CRUD endpoints (Create, Read, Update, Delete)
- Proper error handling (404, 400)
- JSON responses
- In-memory database
- API documentation endpoint

**Run:**
```bash
pip install flask
python3 rest_api_example.py
```

Then test with:
```bash
# List all users
curl http://localhost:5000/users

# Create a user
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","email":"alice@example.com"}'

# Get a specific user
curl http://localhost:5000/users/1

# Update a user
curl -X PUT http://localhost:5000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice Smith"}'

# Delete a user
curl -X DELETE http://localhost:5000/users/1
```

## How These Were Created

These examples were created by asking the AI Dev Team:
- "Create a simple Python function to calculate fibonacci numbers"
- "Create a simple REST API in Python using Flask with endpoints for user management"

The team analyzed the requests, assigned tasks to appropriate agents, and generated production-ready code with proper error handling and documentation.

## Creating Your Own

1. Launch the AI Dev Team: `./run`
2. Choose Team Collaboration Mode
3. Describe what you want to build
4. The team will coordinate and create it
5. Code will be in the `workspace/` directory
