import ibm_db
import ibm_db_dbi

def dbconnector(options: dict):
    """Database DB2 connection helper
    
    params
    ------
    options : dict
        Key-value pair of database connection settings.
        Required:
            |-- host
            |-- port
            |-- username
            |-- password
            `-- dbname 
    """
    
    host = options["host"]
    port = options["port"]
    username = options["username"]
    password = options["password"]
    dbname = options["dbname"]
    
    dsn = "DRIVER={{IBM DB2 ODBC DRIVER}};" + \
          "DATABASE="+ dbname +";" + \
          "HOSTNAME="+ host +";" + \
          "PORT="+ port +";" + \
          "PROTOCOL=TCPIP;" + \
          "UID="+ username +";" + \
          "PWD="+ password +";"
    
    hdbc = ibm_db.connect(dsn, "", "")
    
    return ibm_db_dbi.Connection(hdbc)