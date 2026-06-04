from flask import Blueprint, jsonify, request, make_response
from ..utils import construir_error
from ..services.imanes import modificar_posicion_iman, listar_imanes, eliminar_iman, listar_imanes_por_pais, obtener_resena_iman, procesar_lote_imanes
from ..validators.imanes import validar_id_iman
from ..validators.lugares import validar_codigo_pais
import json

imanes_bp = Blueprint("imanes", __name__)

@imanes_bp.route("/imanes/<int:id_iman>/posicion", methods=["PATCH", "OPTIONS"])
def cambiar_posicion_iman(id_iman):
    
    # El navegador pregunta antes de tirar el PATCH desde el puerto 8000
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:8000")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization, X-User-Id")
        response.headers.add("Access-Control-Allow-Methods", "PATCH, OPTIONS")
        return response

    #Validacion por header
    id_usuario = request.headers.get('X-User-Id')
    if not id_usuario:
        response = make_response(jsonify(construir_error(
            code="UNAUTHORIZED",
            message="Falta identificacion de usuario.",
            description="La cabecera X-User-Id es obligatoria para realizar esta acción."
        )), 401)
        response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:8000")
        return response

    datos = request.get_json()
    ubicacion_heladera = datos.get("ubicacion_heladera")
    posicion_x = datos.get("posicion_x")
    posicion_y = datos.get("posicion_y")

    if ubicacion_heladera is None or posicion_x is None or posicion_y is None:
        response = make_response(jsonify(construir_error(
            code="BAD_REQUEST",
            message="Faltan datos del posicionamiento",
            description="Los parámetros ubicacion_heladera, posicion_x, posicion_y son obligatorios en el body"
        )), 400)
        response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:8000")
        return response

    try:
        exito = modificar_posicion_iman(id_iman, ubicacion_heladera, posicion_x, posicion_y)
        
        if not exito:
            response = make_response(jsonify(construir_error(
                code="NOT_FOUND",
                message="El imán solicitado no existe",
                description=f"No se encontró ningún imán con el id {id_iman}"
            )), 404)
            response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:8000")
            return response
            
        response = make_response("", 204)
        response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:8000")
        return response

    except Exception as e:
        response = make_response(jsonify(construir_error(
            code="INTERNAL_ERROR",
            message="Error interno del servidor",
            description=str(e)
        )), 500)
        response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:8000")
        return response
    
@imanes_bp.route("/imanes", methods=["GET"])
def obtener_imanes():

    id_usuario = request.headers.get("X-User-Id", type=int)
    ubicacion_param = request.args.get("ubicacion", type=str)

    if not id_usuario:
        return jsonify({
            "status": "error",
            "message": "Falta identificacion de usuario."
        }), 401
    
    try:
        imanes = listar_imanes(id_usuario, ubicacion_param)
        return jsonify(imanes), 200
    
    except Exception as e:
        return jsonify(construir_error(
            code="INTERNAL_ERROR",
            message="Error al obtener los imanes",
            description=str(e)
        )), 500

@imanes_bp.route('/imanes/<int:id_iman>', methods=['DELETE'])
def delete_iman(id_iman):
    try:
        id_iman_validado = validar_id_iman(id_iman)
    except ValueError as e:
        return jsonify(e.args[0]), 400

    eliminado = eliminar_iman(id_iman_validado)

    if not eliminado:
        return jsonify(construir_error(
            code="IMAN_NOT_FOUND",
            message='Imán no encontrado',
            description=f"No existe un imán con id '{id_iman_validado}'"
        )), 404

    return '', 204

@imanes_bp.route('/usuarios/<int:id_usuario>/paises/<codigo_pais>/imanes', methods=['GET'])
def get_imanes_por_usuario_pais(id_usuario, codigo_pais):
    try:
        id_pais_validado = validar_codigo_pais(codigo_pais)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    imanes = listar_imanes_por_pais(id_usuario, id_pais_validado)
    return jsonify(imanes), 200

@imanes_bp.route('/imanes/<id_iman>/resena', methods=['GET'])
def get_resena_iman(id_iman):
    try:
        id_iman_validado = validar_id_iman(id_iman)
    except ValueError as e:
        return jsonify(e.args[0]), 400

    relato = obtener_resena_iman(id_iman_validado)

    if relato is None:
        return jsonify({"relato_texto": ""}), 200

    return jsonify({"relato_texto": relato}), 200

@imanes_bp.route('/imanes/batch', methods=['POST'])
def crear_imanes_batch():
    try:
        id_viaje = request.form.get('id_viaje')

        # El frontend enviará TODA la estructura de datos empaquetada en este string JSON
        imanes_data_str = request.form.get('imanes_data')

        if not id_viaje or not imanes_data_str:
            return jsonify({"errors": [{"message": "Faltan datos obligatorios (id_viaje, imanes_data)."}]}), 400

        id_viaje = int(id_viaje)
        lista_datos = json.loads(imanes_data_str)

        # request.files es un diccionario nativo de Flask con todos los archivos subidos
        archivos_dict = request.files

        # Delegamos la responsabilidad de validación y ejecución
        resultados = procesar_lote_imanes(id_viaje, lista_datos, archivos_dict)

        return jsonify({
            "message": "Lote de imanes procesado con éxito",
            "data": resultados
        }), 201

    except ValueError as ve:
        # Aquí capturamos nuestros errores personalizados de negocio (Dry-Run)
        return jsonify(ve.args[0]), 400
    except json.JSONDecodeError:
        return jsonify({"errors": [{"message": "El formato de los datos de imanes (JSON) es inválido."}]}), 400
    except Exception as e:
        print(f"Error Crítico en POST /imanes/batch: {str(e)}")
        return jsonify({"errors": [{"message": "Error interno del servidor al procesar el lote de imanes."}]}), 500