from flask import Blueprint, jsonify, request
from ..db import get_connection

imanes_bp = Blueprint("imanes", __name__)