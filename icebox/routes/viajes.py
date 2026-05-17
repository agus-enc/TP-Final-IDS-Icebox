from flask import Blueprint, jsonify, request
from ..db import get_connection

viajes_bp = Blueprint("viajes", __name__)