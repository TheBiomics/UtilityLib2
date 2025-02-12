from .file import FileSystemUtility
from ..lib.path import EntityPath

from tqdm.auto import tqdm as _TQDMPB

class DataUtility(FileSystemUtility):
  """DataUtility class
  To provide libraries, references, and methods helpful for quick data processing and filtering
  """

  def __init__(self, *args, **kwargs):
    self.__defaults = {}
    self.__defaults.update(kwargs)
    super().__init__(**self.__defaults)

  # Type of variable (validate)
  def check_instance(self, *args, **kwargs):
    _var = kwargs.get("var", args[0] if len(args) > 0 else None)
    _instances = kwargs.get("instances", args[1] if len(args) > 1 else self.type_numbers)
    return isinstance(_var, _instances)

  type_numbers = (int, float, complex)
  def is_numeric(self, *args, **kwargs):
    """Checks if variable is numeric, int, float, or complex"""
    kwargs.update({"instances": self.type_numbers})
    return self.check_instance(*args, **kwargs)

  type_none = (type(None),)
  def is_none(self, *args, **kwargs):
    """Checks if variable is None"""
    kwargs.update({"instances": self.type_none})
    return self.check_instance(*args, **kwargs)

  type_integers = (int)
  def is_int(self, *args, **kwargs):
    """Checks if variable is integer not float, string or other types"""
    kwargs.update({"instances": self.type_integers})
    return self.check_instance(*args, **kwargs)

  is_digit = is_int

  type_arrays = (list, set, tuple)
  def is_array(self, *args, **kwargs):
    """Check if list, tuple, set, or numpy array"""
    kwargs.update({"instances": self.type_arrays})
    return self.check_instance(*args, **kwargs)

  is_list = is_array
  is_set = is_array
  is_tuple = is_array

  type_non_arrays = (int, float, complex, str, bool)
  def is_singular(self, *args, **kwargs):
    """Checks if not iterable or string, int, or float"""
    kwargs.update({"instances": self.type_non_arrays})
    return self.check_instance(*args, **kwargs)

  is_non_iterable = is_singular

  type_maps = (dict)
  def is_map(self, *args, **kwargs):
    """Checks if dict, named tuple, or dataframe"""
    kwargs.update({"instances": self.type_maps})
    return self.check_instance(*args, **kwargs)

  is_dict = is_map

  def is_named_tuple(self, *args, **kwargs):
    """Checks for named tuple (collections namedtuple)"""
    _var = kwargs.get("var", args[0] if len(args) > 0 else None)
    return isinstance(_var, (tuple)) and hasattr(_var, '_fields')

  type_bools =  (bool)
  def is_bool(self, *args, **kwargs):
    """Checks if variable is a boolean"""
    kwargs.update({"instances": self.type_bools})
    return self.check_instance(*args, **kwargs)

  # Iteration
  _loop_obj = None
  def _loop_with_progress_bar(self, *args, **kwargs):
    _items = kwargs.pop('items', args[0] if len(args) > 0 else [])
    _desc = kwargs.pop('desc', args[1] if len(args) > 1 else "Item")
    _desc_fn = kwargs.pop('desc_fn', args[2] if len(args) > 2 else None)

    with _TQDMPB(_items, **kwargs) as _pb:
      self._loop_obj = _pb
      for _i in _items:
        _pb.desc = _desc_fn(_i) if callable(_desc_fn) else f"{_desc} {_i}"
        _pb.update(1)
        yield _i

  _loop_pb = _loop_with_progress_bar
  loop_pb = _loop_with_progress_bar
  loop  = _loop_with_progress_bar
  ProgressBar  = _loop_with_progress_bar
  PB  = _loop_with_progress_bar

  # DataFrame Functions
  ## Pandas
  def df_reset_columns(self, *args, **kwargs):
    """
      @return reset column multiindex additionally set group index as a column

      @params
      0|df: DataFrame
      1|key: DataFrame.groupby().key

      # Considering data is str
      # Float, int list etc are not tested or handled
    """

    _df = kwargs.get("df", args[0] if len(args) > 0 else None)
    _key = kwargs.get("key", args[1] if len(args) > 1 else None)

    if not any([_df is None, _key]):
      return None

    if _df.columns.nlevels > 1:
      # Unravel multi column df
      _joined_cols = ["__".join(_idx) for _idx in _df.columns.ravel()]
      _df.columns = _joined_cols if len(_joined_cols) == len(_df.columns) else _df.columns
      if _key and (not _key in _df.columns) and (not 'index' in _df.columns):
        _df = _df.reset_index()

    return _df

  def _json_file_to_df(self, *args, **kwargs):
    """JSON structure to DataFrame converter

    :param json|0: JSON file path (string)/object (dict)
    :param map|1: Dot notation of keys to parse (parsable using UL.deepkey) i.e., column to key map e.g. entity|0|metadata|header

    :return: pandas.DataFrame

    """
    _json_path = kwargs.get("json_path", args[0] if len(args) > 0 else None)
    _map = kwargs.get("map", args[1] if len(args) > 1 else None)
    _sep = kwargs.get("sep", args[2] if len(args) > 2 else '.')

    kwargs.setdefault("sep", _sep)
    _result = []

    _json_path = EntityPath(_json_path)

    if _json_path.exists():
      _json = self.read_json(_json_path)
    else:
      self.log_error(f'Please provide valid JSON path {_json}')
      return self.DF(_result)

    for _json_el in _json:
      _row = {}
      if _map and isinstance(_map, (dict)):
        # If column map is provided
        for _column, _dotkey in _map.items():
          _row[_column] = self.get_deep_key(_json_el, _dotkey, **kwargs)
        _result.append(_row)
      elif isinstance(_json_el, (dict)):
        # If column map is not provided
        for _column, _value in _json_el.items():
          _row[_column] = _value
        _result.append(_row)
      else:
        self.log_warning("JSON_TO_DF: Could not process data.")

    return self.DF(_result)

  json_to_df = _json_file_to_df

  def pd_categorical(self, df, col_name, sort=True):
    """
    Arguments:
      0|df: pandas DataFrame
      1|col_name: Column Name
      2|sort: boolean

    Returns:
      (categorical_df, mapping)

    Example:
      _df_cat, _mapping = _PM.pd_categorical(df, 'gender', True)

    """
    df_copy = df.copy()
    if sort:
      df_copy = df_copy.sort_values(col_name)

    column_mapping = {}
    if not df_copy[col_name].dtype.name == 'category':
      df_copy[col_name] = df_copy[col_name].astype('category')
      column_mapping = dict(zip( df_copy[col_name].cat.codes, df_copy[col_name]))
      column_mapping_inverse = zip(column_mapping.values(), column_mapping.keys())
      column_mapping_inverse = dict(column_mapping_inverse)
      df_copy[col_name] = df_copy[col_name].map(column_mapping_inverse)

    column_mapping_df = self.DF({
            'key': column_mapping.keys(),
            'values': column_mapping.values(),
        })

    return (df_copy, column_mapping_df)

  def pd_excel_writer(self, *args, **kwargs):
    _excel = args[0] if len(args) > 0 else kwargs.get("excel")
    _options = args[4] if len(args) > 4 else kwargs.get("pyxl_options", dict())

    _options.update({
      "engine": kwargs.get("engine", "openpyxl"),
      "mode": kwargs.get("mode", "a"),
      "if_sheet_exists": kwargs.get("sheet_exists", "replace"),
    })

    if isinstance(_excel, (str, )): # str or path?
      self.require('pandas', 'PD')
      if not self.exists(_excel):
        del _options['mode']
        del _options['if_sheet_exists']

      return self.PD.ExcelWriter(_excel, **_options)

  def fix_column_names(self, *args, **kwargs):
    _df = args[0] if len(args) > 0 else kwargs.get("df")
    _df.columns = [self.text_to_slug(_col).replace('-', '_') for _col in _df.columns]
    return _df

  def _PD_DF_to_Excel(self, *args, **kwargs):
    """Writes in excel file (Purpose: To write multiple sheets)
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

    """

    _excel_writer = kwargs.get("excel",  args[0] if len(args) > 0 else None)
    _df = kwargs.get("df", args[1] if len(args) > 1 else None)
    _sheet_name = kwargs.get("sheet_name", args[2] if len(args) > 2 else 'DataFrame') # Will be deprecated
    _excel_options = kwargs.get("excel_options", args[3] if len(args) > 3 else {'index': False})

    self.require_from('pathlib', 'Path', 'Path')
    if isinstance(_excel_writer, (str, EntityPath)):
      _excel_writer = self.pd_excel_writer(str(_excel_writer), **kwargs)

    _df.copy().to_excel(_excel_writer, sheet_name=_sheet_name, **_excel_options)
    hasattr(_excel_writer, 'save') and _excel_writer.save()
    _excel_writer.close()
    _excel_writer.handles = None
    return _excel_writer

  to_excel = _PD_DF_to_Excel
  write_excel = _PD_DF_to_Excel

  def DF(self, *args, **kwargs):
    _data = args[0] if len(args) > 0 else kwargs.get("data")
    if self.require("pandas", "PD"):
      return self.PD.DataFrame(_data, **kwargs)

  def _csv_file_to_DF(self, *args, **kwargs):
    """Read comma separated value file and convert to Pandas DataFrame"""
    _file = args[0] if len(args) > 0 else kwargs.get("file")
    if self.require("pandas", "PD"):
      return self.PD.read_csv(_file, **kwargs)

  pd_csv = _csv_file_to_DF
  read_csv = _csv_file_to_DF

  def pd_sql_table(self, *args, **kwargs):
    _table_name = kwargs.pop('table_name', args[0] if len(args) > 0 else None)
    _engine = kwargs.pop('engine', args[1] if len(args) > 1 else self.engine)
    if _table_name and _engine and self.require('pandas', 'PD'):
      return self.PD.read_sql_table(_table_name, _engine, **kwargs)

    return None

  def _tsv_file_to_DF(self, *args, **kwargs):
    """Read tab delimited value file and convert to Pandas DataFrame"""
    kwargs['sep'] = "\t"
    return self.pd_csv(*args, **kwargs)

  read_tsv = _tsv_file_to_DF
  pd_tsv = _tsv_file_to_DF

  def _PD_read_excel(self, *args, **kwargs):
    """
    @params
    :param excel_path|0: Either openpyxl writer or path to excel
    :param sheet_name|1: Name of the sheet

    :return: pandas.DataFrame|None

    Example:
      .read_excel(<path.xlsx>, _df, 'sheet_name', **excel_options, **pyxl_options)

    """

    _excel_path = kwargs.get("excel_path", args[0] if len(args) > 0 else None)
    _sheet_name = kwargs.get("sheet_name", args[1] if len(args) > 1 else None)
    kwargs['sheet_name'] = _sheet_name

    if self.is_none(_excel_path):
      return None

    self.require('pandas', 'PD')
    _excel = self.PD.read_excel(_excel_path, **kwargs)

    return _excel

  from_excel = _PD_read_excel
  read_excel = _PD_read_excel
  pd_excel = _PD_DF_to_Excel # Will be migrated to read excel instead of reading i.e., pd_excel = from_excel

  def sync_excel_sheet(self, *args, **kwargs):
    """Reads excel sheet if exists else writes DataFrame to the sheet
      Use other methods to read write or overwrite.
    """
    _excel_path = kwargs.get("excel_path", args[0] if len(args) > 0 else None)
    _sheet_name = kwargs.get("sheet_name", args[1] if len(args) > 1 else None)
    kwargs['sheet_name'] = _sheet_name

    _excel_path = EntityPath(_excel_path)

    if _excel_path.exists() and _excel_path.suffixe in ['.xlsx', '.xls']:
      return self.read_excel(*args, **kwargs)
    else:
      return self.to_excel(*args, **kwargs)

  # Helpers

  def preprocess_output(self, *args, **kwargs):
    """
      @ToDo: Test and QA
    """
    _value = args[0] if len(args) > 0 else kwargs.get("value")
    _callback = args[1] if len(args) > 1 else kwargs.get("callback")
    if _callback and _value:
      return _callback(_value)

    return _value

  def sort_numeric(self, *args, **kwargs):
    """Sort list of iterators as integer values

      @params
      0|iterator: iterator of string values

      @return
      list of sorted values
    """
    _it = kwargs.get("it", args[0] if len(args) > 0 else [])
    _it = list(_it)
    _it.sort(key=self.digit_only)
    return _it

  def parse_digits(self, *args, **kwargs):
    """Digit parts of a given data

      @params
      0|string: String type

      # Considering data is str
      # Float, int list etc are not tested or handled
    """
    _string = args[0] if len(args) > 0 else kwargs.get("string")
    return "".join([_s for _s in str(_string) if _s.isdigit()])

  digits = parse_digits
  digit_only = parse_digits
  parseInt = parse_digits
  parse_int = parse_digits

  def re_compile(self, *args, **kwargs):
    _pattern = args[0] if len(args) > 0 else kwargs.get("pattern")
    _ignore_case = args[1] if len(args) > 1 else kwargs.get("ignore_case", True)
    _escape = args[2] if len(args) > 2 else kwargs.get("escape", False)

    if self.require("re", "REGEX"):
      _pattern = self.REGEX.escape(_pattern) if _escape else _pattern
      _ignore_case = [self.REGEX.I] if _ignore_case else []
      return self.REGEX.compile(_pattern, *_ignore_case)
    else:
      return None

  _toml_default_include = True
  _toml_exclude_private_keys = True

  def _default_toml_str_func(self, data, *args, **kwargs):
    if data is None:
      return None, False

    if isinstance(data, (EntityPath)):
      data = EntityPath(data).full_path

    if not isinstance(data, (str, float, int, bool)):
      data = str(data)

    return data, True

  def recursive_map(self, data, func=None, key=None):
    """Recusrively maps a function to values of Map or Iterables
    Also handles filtering of values (except map)

    :params func
      return valid:
        None (if nothing is returned will act as filter)
        value
        value, if_included (tuple with if value should be included or not)

    """

    if func is None or not callable(func):
      func = print

    from collections.abc import Mapping

    if isinstance(data, Mapping):
      _new_data = type(data)()
      for _k, _v in data.items():
        if self._toml_exclude_private_keys and isinstance(_k, (str)) and _k.startswith("_"):
          continue

        _new_val = self.recursive_map(_v, func, _k)

        # self._toml_default_include???
        if not _new_val is None:
          _new_data[_k] = _new_val

      return _new_data
    elif isinstance(data, (list, tuple)):
      return type(data)(self.recursive_map(item, func, idx) for idx, item in enumerate(data) if item is not None)
    elif DataUtility.is_iterable(data):
      return type(data)(self.recursive_map(item, func, key) for item in data)
    else:
      result = func(data, key)

      if isinstance(result, (tuple, list)) and len(result) == 2:
        _new_value, _include = result
      else:
        _new_value, _include = result, self._toml_default_include

      return _new_value if _include else None

  @staticmethod
  def filter(*args, **kwargs):
    """
      @status: WIP

      @method
      Recursively filter

      @params
      0|data: List/Tuple/Set/Dict(values)/str
      1|what: What char to strip
    """
    _data = kwargs.get("data", args[0] if len(args) > 0 else None)
    _what = kwargs.get("what", args[1] if len(args) > 1 else '')
    _result = []
    if isinstance(_data, (str)):
      ...
    elif isinstance(_data, (list, tuple, set)):
      # Filter for a key word
      for _i in _data:
        if _what in _i:
          _result.append(_i)
    elif isinstance(_data, (dict)):
      for _key, _value in _data:
        ...
    return _result

  @staticmethod
  def strip(*args, **kwargs):
    """
      @method
      Recursively strips string in a array

      @params
      0|data: List/Tuple/Set/Dict(values)/str
      1|char: What char to strip
    """
    _data = kwargs.get("data", args[0] if len(args) > 0 else None)
    _char = kwargs.get("char", args[1] if len(args) > 1 else None)

    if isinstance(_data, (str)):
      _data = _data.strip(_char) if _char and len(_char) > 0 else _data.strip()
    elif isinstance(_data, (list, tuple, set)):
      _data = [DataUtility.strip(_t, _char) for _t in _data]
    elif isinstance(_data, (dict)):
      for _key, _value in _data:
        _data[_key] = DataUtility.strip(_value, _char)

    return _data

  def find_all(self, *args, **kwargs):
    """Finds all substrings in a given string
    """
    _string = kwargs.get("string", args[0] if len(args) > 0 else "")

    # Pop first element to extend re_compile method
    args = args[1:]
    _re_compiled = self.re_compile(*args, **kwargs)

    if _re_compiled is not None:
      return _re_compiled.findall(_string)
    return None

  re_find_all = find_all

  def slice(self, *args, **kwargs):
    """@function (similar to chunks)
    generator method to yield list values in chunks

    @arguments
    0|obj: DF, str, dict, obj or tuple
    1|size: chunk size to yield

    """
    _obj = kwargs.get("obj", args[0] if len(args) > 0 else None)

    if _obj is None:
      return _obj

    from itertools import islice
    return islice(_obj, *args[1:])

  def chunks(self, *args, **kwargs):
    """@function
    generator method to yield list values in chunks

    @arguments
    0|obj: DF, str, dict, obj or tuple
    1|size: chunk size to yield

    """
    _obj = kwargs.get("obj", args[0] if len(args) > 0 else None)
    _size = kwargs.get("size", args[1] if len(args) > 1 else 10)
    if _obj is None or not hasattr(_obj, '__iter__'):
      return _obj

    for _n in range(0, len(_obj), _size):
      yield _obj[_n:_n+_size]

  slices = chunks
  sliced = chunks

  def iterate(self, *args, **kwargs):
    """Flattens and iterates the *args only if they pass is_iterable"""

    _iterables = filter(self.is_iterable, args)
    _iterables = self.flatten(_iterables)

    for _i in _iterables:
      yield _i

  loop = iterate

  @staticmethod
  def is_iterable(*args, **kwargs):
    """
      Checks for iterables except str
    """
    _obj = kwargs.get("obj", args[0] if len(args) > 0 else None)
    return hasattr(_obj, '__iter__') and not isinstance(_obj, (str, bytes))

  @staticmethod
  def flatten(_nested, _level=99, _depth=0):
    """Flattens nested iterables except str

      @usage
      .flatten(list|tuple, 2)
    """
    _collector = []
    _depth += 1
    if all([DataUtility.is_iterable(_nested), not _level <= _depth]):
      for _item in _nested:
        _val = DataUtility.flatten(_item, _level, _depth)
        _collector.extend(_val) if DataUtility.is_iterable(_val) else _collector.append(_val)
    else:
      _collector = _nested
    return _collector

  def product(self, *args, **kwargs):
    """@generator Provides combinations of the given items
      NOTE: Single string will be converted to one item list
      "AUGC" will behave like ["A", "U", ...]
      ["AUGC"] will be treated as it is

      @params
      :param items|*: (list) Object(s) to unpack using *
      :param repeat: (1|int)

      @example
      product("AU", "GC")
      product("AUGC", repeat=3)
      product(["AU", "GC"], repeat=2)
      product(["A", "U", "G", "C"], repeat=8)

    """
    _items = kwargs.get("items", args)
    _items = [str(_s) if self.is_numeric(_s) else _s for _s in _items]

    self.require("itertools", "IT")
    return self.IT.product(*_items, **kwargs)

  def combinations(self, *args, **kwargs):
    """
      @returns combinations of a list.
    """
    _items = kwargs.get("items", args[0] if len(args) > 0 else [])
    _repeat = kwargs.get("repeat", args[1] if len(args) > 1 else 1)
    self.require("itertools", "IT")
    return self.IT.combinations(_items, _repeat)

  def get_parts(self, *args, **kwargs):
    _text = kwargs.get("text", args[0] if len(args) > 0 else None)
    _position = kwargs.get("position", args[1] if len(args) > 1 else -3)
    _delimiter = kwargs.get("delimiter", args[2] if len(args) > 2 else "/")

    _text = str(_text).split(_delimiter)
    return _text[_position]

  def common_substrings(self, *args, **kwargs):
    """
      Returns all common substrings in two given strings

      @params
      0|text1
      1|text2
      2|min_len
      @return
      list

    # DiffMatcher not working as expected
    # from difflib import SequenceMatcher
    # _seq_match = SequenceMatcher(None, _text1, _text2)
    # _match_blocks = _seq_match.get_matching_blocks()
    # _results = [_text1[_b.a: _b.a + _b.size] for _b in _match_blocks if _b.size >= _min_len]

    """

    _text1 = kwargs.get("text1", args[0] if len(args) > 0 else None)
    _text2 = kwargs.get("text2", args[1] if len(args) > 1 else None)
    _min_len = kwargs.get("min_len", args[2] if len(args) > 2 else 2)

    from itertools import combinations as _C

    _t1_combs = [_text1[x:y] for x, y in _C(range(len(_text1) + 1), r=2)]
    _t2_combs = [_text2[x:y] for x, y in _C(range(len(_text2) + 1), r=2)]

    _count_2 = [(_c, _s) for _c, _s in zip(_t2_combs, [_text1.count(_t) for _t in _t2_combs]) if _s > 0 and len(_c) > _min_len]
    _count_1 = [(_c, _s) for _c, _s in zip(_t1_combs, [_text2.count(_t) for _t in _t1_combs]) if _s > 0 and len(_c) > _min_len]

    self.common_substrings__values = _count_1 + _count_2

    return [_ss for _ss, _c in _count_2 + _count_1]

  def common_substring(self, *args, **kwargs):
    """
      returns largest common substring from CLASS.common_substrings

      @params
      0|text1
      1|text2
      2|min_len

    """
    _results = self.common_substrings(*args, **kwargs)
    _result = max(_results, key=len) if len(_results) > 0 else ""
    return _result

  def get_deep_key(self, *args, **kwargs):
    """Get method to access nested key

      @params
      0|obj: dictionary
      1|keys: string, pipe separated string, list, tuple, set
      2|default:
      3|sep: '|'

      @example
      get_deep_key(_dict, (key, subkey, subsubkey), _default)

      @return
      matched key value or default

      @updated 20240517: numbers as string
    """
    _obj = args[0] if len(args) > 0 else kwargs.get("obj", {})
    _keys = args[1] if len(args) > 1 else kwargs.get("keys", ())
    _default = args[2] if len(args) > 2 else kwargs.get("default")
    _sep = args[3] if len(args) > 3 else kwargs.get("sep", "|")

    _instance_list = (tuple, set, list)
    _instance_dict = (dict)
    _instance_singluar = (str, int)

    _keys = _keys if isinstance(_keys, _instance_list) else _keys.split(_sep)

    for _k in _keys:
      # hasattr(, 'get') & str|int=> _dict key, int => list, tuple, or set
      if "*" in _k:
        _obj = list(_obj)
      elif isinstance(_obj, _instance_dict) and isinstance(_k, _instance_singluar):
        _obj = _obj.get(_k, _default)
      elif(isinstance(_obj, _instance_list) and (isinstance(_k, _instance_singluar) or _k.isnumeric())):
        _k = int(_k)
        if len(_obj) > _k:
          _obj = _obj[_k]

    return _obj

  dotkey_value = get_deep_key

  def clean_key(self, *args, **kwargs):
    """Cleans a string to be used a key

      @params
      0|text:
      1|keep:

      @ToDo:
      - Remove special characters
      - remove bracket content flag
      - preserve or replace space with dash or underscore???

    """
    _text = kwargs.get("text", args[0] if len(args) > 0 else "")
    _keep = kwargs.get("keep", args[1] if len(args) > 1 else " ")

    # Compile or get the existing object
    self.re_underscore = self.re_underscore if hasattr(self, "re_underscore") else self.re_compile("_")
    self.re_bracket = self.re_bracket if hasattr(self, "re_bracket") else self.re_compile("\(.*?\)|\[.*?\]")
    self.re_space = self.re_space if hasattr(self, "re_space") else self.re_compile("\s+")

    # _text = _text.lower()
    _text = self.re_bracket.sub(" ", _text)
    _text = self.re_underscore.sub(" ", _text)
    _text = self.re_space.sub(" ", _text.strip())
    return _text

  def expand_ranges(self, *args, **kwargs):
    # 33-51,103-203
    _ranges = args[0] if len(args) > 0 else kwargs.get("ranges", "")
    _expanded = self.flatten(map(
        lambda _l: [*range(int(_l[0]), int(_l[1] or _l[0]) + 1, 1)],
        map(lambda _x: _x.split("-"), _ranges.split(","))
    ))
    return _expanded

  def text_to_slug(self, *args, **kwargs):
    _text = kwargs.get("text", args[0] if len(args) > 0 else "")
    _keep = kwargs.get("keep", args[1] if len(args) > 1 else ["-"])
    _replace_with = kwargs.get("replace_with", args[2] if len(args) > 2 else "-")
    _replacements = kwargs.get("replacements", args[3] if len(args) > 3 else {"_": "-"})
    _lower = kwargs.get("lower", args[4] if len(args) > 4 else False)

    if isinstance(_text, (str)):
      _text = "".join([_c if _c.isalnum() or _c in _keep else _replace_with for _c in _text])
      if isinstance(_replacements, (dict)):
        for _k, _v in _replacements.items():
          _text = _text.replace(_k, _v)

    return _text.lower() if _lower else _text

  slug = text_to_slug

  string_separators = [',', ';', ' ', '\n']
  def _guess_separator(self, *args, **kwargs):
    """Guesses the separator used in a string of values based on the maximum occurrences."""

    _string = kwargs.get('content', args[0] if len(args) > 0 else "")
    _separators = kwargs.get('separators', args[1] if len(args) > 1 else self.string_separators)

    if not self.is_iterable(_separators):
      _separators = list(str(_separators))

    _max_count = 0
    _best_sep = None

    for _sep in _separators:
      _count = _string.count(_sep)
      if _count > _max_count:
        _max_count = _count
        _best_sep = _sep

    return _best_sep

  def split_guess(self, *args, **kwargs):
    """Splits a string of values using the guessed separator."""

    _string = kwargs.get('content', args[0] if len(args) > 0 else "")
    _sep = self._guess_separator(*args, **kwargs)
    _vals = _string.split(_sep)
    return _vals

  def print_csv(self, *args, **kwargs):
    _args = [str(_a) for _a in self.flatten(args)]
    _sep = kwargs.get("sep", ",")
    _return = kwargs.get('ret', True)
    _str = _sep.join(_args)
    if _return:
      return _str
    print(_str)

  format_csv = print_csv
