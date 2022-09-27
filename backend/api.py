"""
api.py
- provides the API endpoints for consuming and producing
  REST requests and responses
"""

from flask import Blueprint, request, jsonify

api = Blueprint('api', __name__)
