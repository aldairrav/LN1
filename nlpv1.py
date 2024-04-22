import openai
import psycopg2
from configparser import ConfigParser

# Configura tu clave API de OpenAI aquí
openai.api_key = 'api_key'


# Función para convertir la entrada en lenguaje natural a SQL utilizando detalles específicos de la base de datos
def natural_language_to_sql(question):
    db_description = """
    Tu respuesta deber ser unicamente la consulta en sql
    En una base de datos de un sistema de punto de venta, la tabla principal es "pos_order". Esta tabla almacena pedidos y tiene las siguientes columnas con sus respectivos significados:
    - "partner_id": ID del cliente vinculado a la venta, referenciado a la tabla "public.res_partner".
    - "session_id": ID del turno de caja que realizó la venta, referenciado a la tabla "public.pos_session".
    - "create_uid": ID del usuario que creó el registro, referenciado a la tabla "public.res_users".
    - "write_uid": ID del usuario que modificó el registro por última vez, referenciado a la tabla "public.res_users".
    - "state": Estado del pedido, que puede ser "new" para nuevo, "paid" para pagado, o "done" para cerrado y contabilizado.
    - "amount_tax": Importe total de impuestos de la venta.
    - "amount_total": Importe total del comprobante de venta.
    - "amount_paid": Total que ha sido pagado, pudiendo ser parcial por pagos a crédito.
    - "amount_return": Total que ha sido reembolsado, en caso de producirse un reembolso.
    - "date_order": Fecha de creación del pedido, en formato UTC.
    - "cashier": Cajero que realizó el pedido.
    - "location_id": ID del lugar de extracción del inventario, referenciado a la tabla "public.stock_location".
    - "tipo_comp": Tipo de comprobante de la venta.
    - "num_comp": Número del comprobante.
    """
    
    # Prepara el prompt para el modelo de chat
    prompt = f"{db_description} Basado en esta estructura, {question}"
    
    # Utiliza el endpoint de chat para hacer la solicitud
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[
            {"role": "system", "content": db_description},
            {"role": "user", "content": question}
        ], temperature=0
    )
    
    # Extrae y retorna la respuesta del modelo
    if response and response['choices']:
        return response['choices'][0]['message']['content'].strip()
    else:
        return "No se pudo generar la consulta SQL."


# Función para ejecutar la consulta SQL y obtener resultados
def execute_query(query):
    conn = psycopg2.connect(
    host="localhost",
    database="mrpan",
    user="postgres",
    password="postgres",
    port="5433"  # Especifica el puerto aquí
)
    result = None
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchall()  # Ajustar según el tipo de consulta
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result

# Función principal para el asistente
def main():
    user_query = input("Por favor, introduce tu consulta en lenguaje natural: ")
    sql_query = natural_language_to_sql(user_query)
    print(f"Consulta SQL generada: {sql_query}")
    results = execute_query(sql_query)
    if results:
        for row in results:
            print(row)  
    else:
        print("No se encontraron resultados.")

if __name__ == "__main__":
    main()
