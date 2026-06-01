from rembg import remove
from ..utils import construir_error

def procesar_iman_ia(archivo_flask) -> bytes:
    """
    Toma el archivo subido por el usuario, le quita el fondo utilizando IA,
    y devuelve los bytes puros en formato PNG transparente.
    """
    try:
        # 1. Leemos los bytes crudos directamente de la petición de Flask
        input_bytes = archivo_flask.read()

        # 2. La IA de rembg recibe bytes y devuelve bytes (ya en formato PNG)
        output_bytes = remove(input_bytes)

        # 3. Devolvemos la salida lista para ser inyectada en Supabase
        return output_bytes

    except Exception as e:
        print(f"Error interno IA: {str(e)}")
        raise ValueError({"errors": [
            construir_error(
                code="ia_processing_error",
                message="Error al procesar el imán.",
                description="Falló la remoción de fondo mediante IA."
            )]}, 500)