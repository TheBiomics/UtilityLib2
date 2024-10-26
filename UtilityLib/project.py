from .utility import UtilityManager
from .lib.obj import ObjDict
from .lib.path import EntityPath

class ProjectManager(UtilityManager):
  name = "project"
  config_version = 1
  config_subversion = 20241000
  path_config = None

  def __init__(self, *args, **kwargs):
    self.__defaults = {"config_key": "config"}
    self.__defaults.update(kwargs)
    super().__init__(**self.__defaults)
    self.load_config()

  def _toml_map_from_str(self, data):
    if isinstance(data, dict):
      data = {k: self._toml_map_from_str(v) for k, v in data.items()}
    elif isinstance(data, list):
      data = [self._toml_map_from_str(v) for v in data]
    elif data == "":
      data = None

    return data

  def create_file_backup(self, *args, **kwargs):
    _path_file = kwargs.get('path_file', args[0] if len(args) > 0 else None)
    _path_backup = kwargs.get('path_backup', args[1] if len(args) > 1 else None)

    _path_file = EntityPath(_path_file)
    _path_backup = EntityPath(_path_backup)

    if _path_file is None or not _path_file.exists():
      return

    if not _path_backup.exists():
      # It's a backup file path
      if not _path_backup.parent().exists():
        _path_backup.parent().validate()
    else:
      _path_backup = _path_backup / _path_file.with_suffix(f'.{self.timestamp}{_path_file.suffix}').name

    _path_file.copy(_path_backup)

    return _path_backup.exists()

  def get_file_backups(self, *args, **kwargs):
    _path_file = kwargs.get('path_file', args[0] if len(args) > 0 else None)
    _path_file = EntityPath(_path_file)
    _path_backup = kwargs.get('path_backup', args[1] if len(args) > 1 else _path_file if _path_file.is_dir() else _path_file.parent())
    _path_backup = EntityPath(_path_backup)

    return _path_backup.search(f"{_path_file.stem}*{_path_file.suffix}")

  def get_file_backup(self, *args, **kwargs):
    """Get latest file backup"""
    *_backups, = self.get_file_backups(*args, **kwargs)
    sorted(_backups, key=lambda _x: self.get_parts(_x, -2, '.'), reverse=True)
    return _backups[0] if len(_backups) > 0 else None

  toml_path = "~/UtilityLib-Project.toml"
  toml_data = ObjDict()

  def read_toml(self, *args, **kwargs):
    """Reads .toml file content and parses into dict"""
    self.toml_path = kwargs.get('toml_path', args[0] if len(args) > 0 else self.toml_path)
    self.toml_path = EntityPath(self.toml_path)

    if self.toml_path.exists() and self.require('toml', 'TOML'):
      _raw = self.TOML.load(self.toml_path)
      self.toml_data = ObjDict(self._toml_map_from_str(_raw))

    return self.toml_data

  load_toml = read_toml
  get_toml = read_toml
  from_toml = read_toml

  def _default_toml_str_func(self, data, *args, **kwargs):
    if data is None:
      return None, False

    return super()._default_toml_str_func(data)

  def convert_to_toml_obj(self, data={}) -> str:
    _toml_str = ""
    if data and self.require('toml', 'TOML'):
      self.log_debug('PROJECT_01: Dumping TOML data')
      _toml_str = self.recursive_map(data)
      _toml_str = data
      _toml_str = self.TOML.dumps(_toml_str)

    return _toml_str

  def write_toml(self, *args, **kwargs):
    """Writes given object to the provided path"""
    self.toml_path = kwargs.get('toml_path', args[0] if len(args) > 0 else self.toml_path)
    self.toml_data = kwargs.get('toml_data', args[1] if len(args) > 1 else self.toml_data)
    self.toml_path = EntityPath(self.toml_path)

    _toml_str = self.convert_to_toml_obj(self.toml_data)

    if self.toml_path.exists():
      self.log_debug('PROJECT_02: Overwriting TOML config.')

    self.toml_path.write(_toml_str)
    return self.toml_path.exists()

  to_toml = write_toml

  def set_config_path(self, *args, **kwargs):
    self.update_attributes(self, kwargs)
    self.path_config = (EntityPath(self.path_base) / self.name).with_suffix(f".v{self.config_version}.{self.config_subversion}.config.gz") if self.path_base else EntityPath(f"{self.name}.v{self.config_version}.{self.config_subversion}.config.gz")

  def rebuild_config(self, *args, **kwargs):
    self.update_attributes(self, kwargs)
    """Read config again"""
    setattr(self, self.config_key, self.ConfigManager(getattr(self, self.config_key, ObjDict())))

  def reset_config(self, *args, **kwargs):
    self.update_attributes(self, kwargs)
    return self.load_config(**kwargs)

  def load_config(self, *args, **kwargs):
    self.update_attributes(self, kwargs)
    if not getattr(self, 'path_config'):
      self.set_config_path()

    self.ConfigManager = ObjDict
    setattr(self, self.config_key, self.ConfigManager())

    if self.check_path(self.path_config):
      setattr(self, self.config_key, self.unpickle(self.path_config))

    self.rebuild_config()

  def save_config(self, *args, **kwargs):
    return self.update_config(*args, **kwargs)

  def update_config(self, *args, **kwargs):
    self.update_attributes(self, kwargs)
    self.set_config_path()
    self.rebuild_config()

    _config = getattr(self, self.config_key, ObjDict())
    _config.last_updated = self.timestamp
    self.pickle(self.path_config, _config)

  def get_path(self, *args, **kwargs):
    _relative_path = args[0] if len(args) > 0 else kwargs.get("path", "")
    _fp = str(_relative_path).lstrip('/')
    if not self.path_base is None:
      _fp = EntityPath(self.path_base) / _fp
    return _fp

  def get_join(self, *args, **kwargs):
    _key = args[0] if len(args) > 0 else kwargs.get("key", None)
    _val = args[1] if len(args) > 1 else kwargs.get("val", None)
    _glue = args[2] if len(args) > 2 else kwargs.get("glue", "/")
    _def_prepend = args[3] if len(args) > 3 else kwargs.get("default", "")

    if not _key is None:
      _static_config = getattr(self, self.config_key)
      _def_prepend = _static_config.get(_key, "")

    return f"{_glue}".join([_def_prepend, _val])

  def _apply_method_to_file(self, file_ref, operation, *args, **kwargs):
    """All operations are not op_file compatible due to variable number of arguments

      @params
      file_ref
      op
      *args: Passed to the method
      **kwargs: Passed on to the method

    """

    file_ref = kwargs.pop('file_ref', None) or file_ref
    operation = kwargs.pop('op', None) or operation

    _file_path = self.get_path(file_ref)
    _op = getattr(self, operation)

    return _op(_file_path, *args, **kwargs)

  file_op = _apply_method_to_file
  file_operation = _apply_method_to_file
  func_on_file = _apply_method_to_file
  file_func = _apply_method_to_file
  op_file = _apply_method_to_file
