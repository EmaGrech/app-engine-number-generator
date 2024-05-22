from flask import Flask, jsonify, request
import random
import sqlalchemy
from google.cloud.sql.connector import Connector
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Configure database connection
def connect():
    logging.info("Establishing database connection...")
    connector = Connector()
    conn = connector.connect(
        "fifth-glazing-422823-j5:europe-west1:generator-history",
        "pymysql",
        user="root",
        password="pass",
        db="Numbers_Generated"
    )
    logging.info("Database connection established.")
    return conn


#number generation
@app.route('/generate', methods=['POST'])
def generate():
    logging.info("Generating random numbers...")
    #connecting to database    
    conn = connect()
    cursor = conn.cursor()
    instance = request.args.get('instance')

    #number generation    
    numbers = [(random.randint(0, 100000), instance) for _ in range(1000)]

    #commits numbers to database
    cursor.executemany(
        "INSERT INTO numbers_generated (number, instance) VALUES (%s, %s)",
        numbers
    )
    conn.commit()

    #closing cursor and connection
    cursor.close()
    conn.close()

    logging.info("Random numbers generated and stored.")
    return jsonify({"status": "success", "instance": instance, "numbers": len(numbers)})

#displaying results
@app.route('/results', methods=['GET'])
def results():
    logging.info("Fetching results...")
    #connecting to database 
    conn = connect()
    cursor = conn.cursor()

    #traversing database and outputting results
    cursor.execute("SELECT instance, COUNT(*), MAX(number), MIN(number) FROM numbers GROUP BY instance")
    results = cursor.fetchall()

    #closing cursor and connection
    cursor.close()
    conn.close()

    #outputting results
    output = {
        "instances": [{"instance": row[0], "count": row[1], "max": row[2], "min": row[3]} for row in results]
    }
    logging.info("Results fetched successfully.")
    return jsonify(output)


if __name__ == '__main__':
    logging.info("Starting Flask application...")
    app.run(host='0.0.0.0', port=8080)