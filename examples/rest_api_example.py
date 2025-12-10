#!/usr/bin/env python3
"""
Example: Simple REST API with Flask
Created by AI Dev Team Demo
"""

from flask import Flask, jsonify, request, abort
from datetime import datetime

app = Flask(__name__)

# In-memory database
users = {}
user_id_counter = 1


@app.route('/')
def home():
    """API home endpoint."""
    return jsonify({
        'name': 'User Management API',
        'version': '1.0',
        'endpoints': {
            'GET /users': 'List all users',
            'GET /users/<id>': 'Get specific user',
            'POST /users': 'Create new user',
            'PUT /users/<id>': 'Update user',
            'DELETE /users/<id>': 'Delete user'
        }
    })


@app.route('/users', methods=['GET'])
def list_users():
    """List all users."""
    return jsonify({
        'count': len(users),
        'users': list(users.values())
    })


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user."""
    if user_id not in users:
        abort(404, description=f'User {user_id} not found')
    return jsonify(users[user_id])


@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user."""
    global user_id_counter
    
    if not request.json or 'name' not in request.json:
        abort(400, description='Name is required')
    
    user = {
        'id': user_id_counter,
        'name': request.json['name'],
        'email': request.json.get('email', ''),
        'created_at': datetime.now().isoformat()
    }
    
    users[user_id_counter] = user
    user_id_counter += 1
    
    return jsonify(user), 201


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an existing user."""
    if user_id not in users:
        abort(404, description=f'User {user_id} not found')
    
    if not request.json:
        abort(400, description='No data provided')
    
    user = users[user_id]
    user['name'] = request.json.get('name', user['name'])
    user['email'] = request.json.get('email', user['email'])
    user['updated_at'] = datetime.now().isoformat()
    
    return jsonify(user)


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user."""
    if user_id not in users:
        abort(404, description=f'User {user_id} not found')
    
    del users[user_id]
    return jsonify({'message': f'User {user_id} deleted'}), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': str(error.description)}), 404


@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors."""
    return jsonify({'error': str(error.description)}), 400


if __name__ == '__main__':
    print("🚀 Starting User Management API...")
    print("📍 Running on http://localhost:5000")
    print("\nExample requests:")
    print("  curl http://localhost:5000/")
    print("  curl http://localhost:5000/users")
    print('  curl -X POST http://localhost:5000/users -H "Content-Type: application/json" -d \'{"name":"Alice","email":"alice@example.com"}\'')
    print("  curl http://localhost:5000/users/1")
    print()
    
    app.run(debug=True, port=5000)
