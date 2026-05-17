from flask import Blueprint, jsonify, request
from ..db import get_connection

lugares_bp = Blueprint("lugares", __name__)