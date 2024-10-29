class DataUtility(UtilityLib.core.file.FileSystemUtility)
  DataUtility(*args, **kwargs)

  ## MRO:
      DataUtility
      UtilityLib.core.file.FileSystemUtility
      UtilityLib.core.db.DatabaseUtility
      UtilityLib.core.cmd.CommandUtility
      UtilityLib.core.log.LoggingUtility
      UtilityLib.core.time.TimeUtility
      UtilityLib.BaseUtility
      builtins.object

  ## Methods:

  DF(self, *args, **kwargs): Invokes Pandas DataFrame

  PB = _loop_with_progress_bar(self, *args, **kwargs)

  ProgressBar = _loop_with_progress_bar(self, *args, **kwargs)

  __init__(self, *args, **kwargs)
      Initialize self.  See help(type(self)) for accurate signature.

  check_instance(self, *args, **kwargs)

  chunks(self, *args, **kwargs)
      @function
      generator method to yield list values in chunks

      @arguments
      0|obj: DF, str, dict, obj or tuple
      1|size: chunk size to yield

  clean_key(self, *args, **kwargs)
      Cleans a string to be used a key

      @params
      0|text:
      1|keep:

      @ToDo:
      - Remove special characters
      - remove bracket content flag
      - preserve or replace space with dash or underscore???

  combinations(self, *args, **kwargs)
      @returns combinations of a list.

  common_substring(self, *args, **kwargs)
      returns largest common substring from CLASS.common_substrings

      @params
      0|text1
      1|text2
      2|min_len

  common_substrings(self, *args, **kwargs)
        Returns all common substrings in two given strings

        @params
        0|text1
        1|text2
        2|min_len
        @return
        list

  df_reset_columns(self, *args, **kwargs)
      @return reset column multiindex additionally set group index as a column

      @params
      0|df: DataFrame
      1|key: DataFrame.groupby().key


  digit_only = parse_digits(self, *args, **kwargs)

  digits = parse_digits(self, *args, **kwargs)

  dotkey_value = get_deep_key(self, *args, **kwargs)

  expand_ranges(self, *args, **kwargs)

  find_all(self, *args, **kwargs)
      Finds all substrings in a given string

  fix_column_names(self, *args, **kwargs)

  format_csv = print_csv(self, *args, **kwargs)

  from_excel(self, *args, **kwargs)
      Arguments:
        0|excel: Either openpyxl writer or path to excel
        1|sheet: Name of the sheet

      Returns:
        pandas.DataFrame

      Example:
        _PM.from_excel(<path.xlsx>, _df, 'sheet_name', **excel_options, **pyxl_options)

  get_deep_key(self, *args, **kwargs)
      Get method to access nested key

      @params
      0|obj: dictionary
      1|keys: string, pipe separated string, list, tuple, set
      2|default:
      3|sep: '|'

      @example
      get_deep_key(_dict, (key, subkey, subsubkey), _default)

      @return
      matched key value or default

  get_parts(self, *args, **kwargs)

  is_array(self, *args, **kwargs)
      Check if list, tuple, set, or numpy array

  is_bool(self, *args, **kwargs)
      Checks if variable is a boolean

  is_dict = is_map(self, *args, **kwargs)

  is_digit = is_int(self, *args, **kwargs)

  is_int(self, *args, **kwargs)
      Checks if variable is integer not float, string or other types

  is_list = is_array(self, *args, **kwargs)

  is_map(self, *args, **kwargs)
      Checks if dict, named tuple, or dataframe

  is_named_tuple(self, *args, **kwargs)
      Checks for named tuple (collections namedtuple)

  is_non_iterable = is_singular(self, *args, **kwargs)

  is_numeric(self, *args, **kwargs)
      Checks if variable is numeric, int, float, or complex

  is_set = is_array(self, *args, **kwargs)

  is_singular(self, *args, **kwargs)
      Checks if not iterable or string, int, or float

  is_tuple = is_array(self, *args, **kwargs)

  iterate(self, *args, **kwargs)
      Flattens and iterates the *args only if they pass is_iterable

  json_to_df = _json_file_to_df(self, *args, **kwargs)

  loop = iterate(self, *args, **kwargs)

  loop_pb = _loop_with_progress_bar(self, *args, **kwargs)

  parseInt = parse_digits(self, *args, **kwargs)

  parse_digits(self, *args, **kwargs)
      Digit parts of a given data

      @params
      0|string: String type

  parse_int = parse_digits(self, *args, **kwargs)

  pd_categorical(self, df, col_name, sort=True)
      Arguments:
        0|df: pandas DataFrame
        1|col_name: Column Name
        2|sort: boolean

      Returns:
        (categorical_df, mapping)

      Example:
        _df_cat, _mapping = _PM.pd_categorical(df, 'gender', True)

  pd_csv = _csv_file_to_DF(self, *args, **kwargs)

  pd_excel(self, *args, **kwargs)
      Arguments:
        0|excel: Either openpyxl writer or path to excel
        1|df: Pandas DataFrame to be written
        2|sheet_name: Name of the sheet
        3|excel_options: Options for PD.to_excel e.g., {'index': False, 'float_format': "%.4f"}
        4|pyxl_options: Options (like engine, mode) for PD.ExcelWriter

      Returns:
        openpyxl
        openpyxl.sheets => Contains sheets
        openpyxl.books => contains books

      Example:
        _PM.pd_excel(<path.xlsx>, _df, 'sheet_name', **excel_options, **pyxl_options)

  pd_excel_writer(self, *args, **kwargs)

  pd_sql_table(self, *args, **kwargs)

  pd_tsv = _tsv_file_to_DF(self, *args, **kwargs)

  preprocess_output(self, *args, **kwargs)
      @ToDo: Test and QA

  print_csv(self, *args, **kwargs)

  product(self, *args, **kwargs)
      @generator Provides combinations of the given items
      NOTE: Single string will be converted to one item list
      "AUGC" will behave like ["A", "U", ...]
      ["AUGC"] will be treated as it is

      @params
      0|items (list): Object(s) to unpack using *
      1|repeat (1|int)

      @example
      combination(["AU", "GC"], 1)
      combination(["AUGC"], 8)
      combination(["A", "U", "G", "C"], 8)

  re_compile(self, *args, **kwargs)

  re_find_all = find_all(self, *args, **kwargs)

  read_csv = _csv_file_to_DF(self, *args, **kwargs)

  read_tsv = _tsv_file_to_DF(self, *args, **kwargs)

  recursive_map(self, data, func=None, key=None)
      Recusrively maps a function to values of Map or Iterables
      Also handles filtering of values (except map)

      :params func
        return valid:
          None (if nothing is returned will act as filter)
          value
          value, if_included (tuple with if value should be included or not)

  slice(self, *args, **kwargs)
      @function (similar to chunks)
      generator method to yield list values in chunks

      @arguments
      0|obj: DF, str, dict, obj or tuple
      1|size: chunk size to yield

  sliced = chunks(self, *args, **kwargs)

  slices = chunks(self, *args, **kwargs)

  slug = text_to_slug(self, *args, **kwargs)

  sort_numeric(self, *args, **kwargs)
      Sort list of iterators as integer values

      @params
      0|iterator: iterator of string values

      @return
      list of sorted values

  split_guess(self, *args, **kwargs)
      Splits a string of values using the guessed separator.

  text_to_slug(self, *args, **kwargs)

  ----------------------------------------------------------------------
  Static methods defined here:

  filter(*args, **kwargs)
      @status: WIP

      @method
      Recursively filter

      @params
      0|data: List/Tuple/Set/Dict(values)/str
      1|what: What char to strip

  flatten(_nested, _level=99, _depth=0)
      Flattens nested iterables except str

      @usage
      .flatten(list|tuple, 2)

  is_iterable(*args, **kwargs)
      Checks for iterables except str

      @usage
      .flatten(list|tuple, 2)

  strip(*args, **kwargs)
      @method
      Recursively strips string in a array

      @params
      0|data: List/Tuple/Set/Dict(values)/str
      1|char: What char to strip

  ----------------------------------------------------------------------
  ## Attributes:

  string_separators = [',', ';', ' ', '\n']

  type_arrays = (<class 'list'>, <class 'set'>, <class 'tuple'>)

  type_bools = <class 'bool'>
      bool(x) -> bool

      Returns True when the argument x is true, False otherwise.
      The builtins True and False are the only two instances of the class bool.
      The class bool is a subclass of the class int, and cannot be subclassed.

  type_integers = <class 'int'>
      int([x]) -> integer
      int(x, base=10) -> integer

      Convert a number or string to an integer, or return 0 if no arguments
      are given.  If x is a number, return x.__int__().  For floating point
      numbers, this truncates towards zero.

      If x is not a number or if base is given, then x must be a string,
      bytes, or bytearray instance representing an integer literal in the
      given base.  The literal can be preceded by '+' or '-' and be surrounded
      by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.
      Base 0 means to interpret the base from the string as an integer literal.
      >>> int('0b100', base=0)
      4

  type_maps = <class 'dict'>
      dict() -> new empty dictionary
      dict(mapping) -> new dictionary initialized from a mapping object's
          (key, value) pairs
      dict(iterable) -> new dictionary initialized as if via:
          d = {}
          for k, v in iterable:
              d[k] = v
      dict(**kwargs) -> new dictionary initialized with the name=value pairs
          in the keyword argument list.  For example:  dict(one=1, two=2)

  type_non_arrays = (<class 'int'>, <class 'float'>, <class 'complex'>, ...

  type_numbers = (<class 'int'>, <class 'float'>, <class 'complex'>)
