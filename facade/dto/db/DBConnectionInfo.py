class DBConnectionInfo:
    database = None
    username = None
    password = None
    host = None
    port = None
    dbtype = None

    def __init__(self, database=None, username=None, password=None, host=None, port=None, dbtype=None):
        self.database = database
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.dbtype = dbtype

    def __str__(self):
        return 'DBConnectionInfo[ database=%s, username=%s, password=%s, host=%s, port=%s, dbtype=%s ]' % (
        self.database, self.username, self.password, self.host, self.port, self.dbtype)
