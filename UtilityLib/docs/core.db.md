class DatabaseUtility(UtilityLib.core.cmd.CommandUtility)
  DatabaseUtility(*args, **kwargs)

  ## MRO:
      DatabaseUtility
      UtilityLib.core.cmd.CommandUtility
      UtilityLib.core.log.LoggingUtility
      UtilityLib.core.time.TimeUtility
      UtilityLib.BaseUtility
      builtins.object

  ## Methods:

  __init__(self, *args, **kwargs)

  connect_mysql(self, *args, **kwargs)

  connect_sqlite(self, *args, **kwargs)
      Connects with SQLite Database

      :param db_path|0: Path to SQLite Database File (Optionally to be created)
      :returns: str|None

  db_connect = connect_sqlite(self, *args, **kwargs)

  get_last_id(self, *args, **kwargs)
      @default
      table_name*
      id_column = "primary_id"
      engine: self.engine
      default: 0 (Default Last ID in case none found.)

      @returns
      max value from the provided `id_column`

  get_table_data(self, *args, **kwargs)
      Get SQLite or SQL Table Data

      * Use where dict object for where query
      * Read whole table, use chunksize for generator object for large tables)

      :param table_name|0: Default First Table
      :param where|1: Where Clause
      :param engine|2: Pass database Engine (Default self.engine)
      :param chunksize: See `pandas.read_sql_table`

      Returns:
        DataFrame|None: Pandas DataFrame

  insert(self, *args, **kwargs)
      @usage
      CLASS.insert("table_name", {
        'col_1': '5vr3',
        'col_2': 'DB12070',
        ...
        'col_N': None})

  query_datbase = _query_database(self, *args, **kwargs)

  query_db = _query_database(self, *args, **kwargs)

  set_table_data(self, *args, **kwargs)
      Function for pandas to update/insert table data using the initiated SQLite/MySQL engine
      [Ref](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html)

      @params
      3|if_exists: append|replace

  set_table_info(self, *args, **kwargs)

  sql_query = _query_database(self, *args, **kwargs)

  ----------------------------------------------------------------------
  ## ReadOnlyProperties:

  tables
