import logging
import pyodbc
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusException

# Set up logging to a file called 'rtu_data.log' with level INFO
logging.basicConfig(filename='rtu_data.log', level=logging.INFO)

# Create a new Modbus client that will connect to the RTU at the specified IP address
client = ModbusTcpClient('192.168.1.10')  # Replace with your RTU's IP address

# Set up a connection to the SQL Server database using pyodbc
# Replace the placeholders in the connection string with your actual server name, database name, username, and password
conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=server_name;'
    r'DATABASE=database_name;'
    r'UID=user;'
    r'PWD=password'
)
cnxn = pyodbc.connect(conn_str)
cursor = cnxn.cursor()

try:
    # Try to connect to the Modbus client (RTU)
    # If the connection fails, log an error and raise a ConnectionError exception
    if not client.connect():
        logging.error('Failed to connect to RTU')
        raise ConnectionError('Could not connect to RTU')

    # Define the range of addresses to read from the RTU
    start_address = 0
    end_address = 10000  # Replace with the actual end address for your RTU

    # Try to read each register in the range
    for address in range(start_address, end_address):
        result = client.read_holding_registers(address, 1)

        # Check if the read was successful
        # If it was, print and log the results, and insert the data into the database
        # If it wasn't, log an error and raise a ModbusException
        if not result.isError():
            print(f'Register {address}: {result.registers}')
            logging.info(f'Read data from RTU: {result.registers}')

            cursor.execute("""
                INSERT INTO table_name (address, data)  # Replace with your table name
                VALUES (?, ?)
            """, address, result.registers[0])
            cnxn.commit()
        else:
            logging.error(f'Failed to read data from RTU at address {address}')
            raise ModbusException(f'Could not read data from RTU at address {address}')

# If a ConnectionError or ModbusException is raised, print and log the error message
except (ConnectionError, ModbusException) as e:
    print(f'Error: {str(e)}')
    logging.error(f'Error: {str(e)}')

# Regardless of whether an error occurred, always close the Modbus client and database connections at the end
finally:
    client.close()
    cnxn.close()
