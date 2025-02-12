from . import __version__, __description__, __build__, __name__
import importlib as MODULE_IMPORTER
import os as _OS
import sys as _SYSTEM
from functools import lru_cache as CacheMethod
from ..lib.path import EntityPath

class BaseUtility:
  __name__= __name__
  __version__= __version__
  __build__= __build__
  __description__= __description__
  name = __name__
  version = __version__
  version_info = f"{__version__}.{__build__}"

  _messages_to_log = [] # [{type:..., text:..., time:...}]

  _imported_modules = []

  def __init__(self, *args, **kwargs):
    __defaults = {}
    __defaults.update(kwargs)
    self.update_attributes(self, __defaults)
    self._set_working_dir(**__defaults)

  _path_base = None
  @property
  def path_base(self):
    if self._path_base is None:
      self._path_base = EntityPath(self.OS.getcwd())
    return self._path_base

  @path_base.setter
  def path_base(self, path):
    self._path_base = EntityPath(path) if path else EntityPath(self.OS.getcwd())

    if self._path_base and self._path_base.exists():
      self.OS.chdir(self._path_base)

  pwd = path_base

  def _set_working_dir(self, *args, **kwargs):
    if hasattr(self, 'path_bases'):
      self.set_project_paths(**kwargs)
    elif hasattr(self, 'path_base') and getattr(self, 'path_base'):
      self.path_base = getattr(self, 'path_base')

  set_cwd = _set_working_dir
  setcwd = _set_working_dir

  def set_project_paths(self, *args, **kwargs):
    """Set current working directory"""
    _path_bases = args[0] if len(args) > 0 else kwargs.get("path_bases", self.path_base)
    # Consider first path for Linux and second path for Windows
    if isinstance(_path_bases, (str)):
      self.path_base = EntityPath(_path_bases)
    elif isinstance(_path_bases, (list, tuple)):
      _path_bases = _path_bases * 2
      self.path_base = _path_bases[1] if self.is_windows else _path_bases[0]
    elif isinstance(_path_bases, (dict)):
      # Consider that order of the dict is preserved
      self.set_project_paths(path_bases=list(_path_bases.values()))

  def is_running(self, *args, **kwargs):
    _file = args[0] if len(args) > 0 else kwargs.get("file", "UtilityLib-Processes-v2.txt")
    _dir = args[1] if len(args) > 1 else kwargs.get("dir", 'Documents/PyProcessConfig')

    _path_user_settings = self.OS.path.join(self.OS.path.expanduser('~'), _dir)
    _path_file_pid = f"{_path_user_settings}/{_file}"

    if not self.OS.path.exists(_path_user_settings):
      self.OS.makedirs(_path_user_settings)

    _current_pid = self.OS.getpid()

    # Import psutil
    from psutil import pid_exists, Process

    if self.OS.path.exists(_path_file_pid):
      with open(_path_file_pid) as f:
        pid = f.read()
        pid = int(pid) if pid.isnumeric() else None
      if pid is not None and pid_exists(pid) and Process(pid).cmdline() == Process(_current_pid).cmdline():
        return True

    with open(_path_file_pid, 'w') as f:
      f.write(str(_current_pid))

    return False

  def _setattrs(self, kw):
    """set multiple attributes from dict"""
    [setattr(self, _k, kw[_k]) for _k in kw.keys()]

  set_attributes = _setattrs
  setattrs = _setattrs

  def update_attributes(self, obj=None, kw: dict={}, defaults: dict={}):
    """Sets and updates object attributes from dict
    """
    if obj is None:
      obj = self

    [setattr(obj, _k, defaults[_k]) for _k in defaults.keys() if not hasattr(obj, _k)]
    [setattr(obj, _k, kw[_k]) for _k in kw.keys()]

  def __call__(self, *args, **kwargs):
    self.update_attributes(self, kwargs)
    return self

  def __repr__(self):
    return f"{self.name}: Use help() function to see the list of all methods."

  __str__ = __repr__

  OS = _OS
  SYS = _SYSTEM
  SYSTEM = _SYSTEM

  @property
  def is_windows(self):
    return self.OS.name == "nt"

  @property
  def is_linux(self):
    return self.OS.name == "posix"

  def _import_module_from(self, *args, **kwargs):
    """Executes "from Package import Module"

    @coverage
    from PIL import Image as PImage <=> import PIL.Image as PImage
    from pathlib import Path as PATH <=> import pathlib; PATH = getattr(pathlib, 'Path')

    @params
    0|package:
    1|module:
    2|as:
    """

    _package = args[0] if len(args) > 0 else kwargs.get("package")
    _module = args[1] if len(args) > 1 else kwargs.get("module")
    _as = args[2] if len(args) > 2 else kwargs.get("as")

    _module_instance = None

    if not _package:
      return None

    try:
      _pkg = MODULE_IMPORTER.import_module(_package)
      if hasattr(_pkg, _module):
        _module_instance = getattr(_pkg, _module)
      else:
        _import_stmt = f"{_package}.{_module}" # "import PIL.Image <=> from PIL import Image"
        _module_instance = MODULE_IMPORTER.import_module(_import_stmt)

    except:
      ...

    if not _module_instance:
      return False

    self._imported_modules.append((_as, ))
    setattr(self, _as, _module_instance)
    return True

  require_from = _import_module_from
  module_from = _import_module_from
  import_from = _import_module_from
  from_import = _import_module_from

  def require_path(self, *args, **kwargs):
    """Imports a module through a path by adding the module path to system path

    @extends require
    To import from a given path by adding the path to the system

    :param module_path|0:
    :param module|1:
    """
    _module_path = kwargs.get("module_path", args[0] if len(args) > 0 else ".")

    args = args[1:] # tuple.pop(0 error)

    self.SYSTEM.path.append(_module_path)
    self._import_single_module(*args, **kwargs)
    return self

  import_path = require_path

  def _import_multiple_modules(self, *args, **kwargs):
    """@extends require
    for multiple imports in single call

    @params
    0|modules: array of tuples|list

    @return
    list containing success status (True|False) of the provided list

    """
    _modules = args[0] if len(args) > 0 else kwargs.get("modules", [])

    self._enabled_modules = []
    for _rm in _modules:
      _res = False
      if len(_rm) > 0 and isinstance(_rm, (tuple, list)):
        _res = self._import_single_module(*_rm, **kwargs)
      self._enabled_modules.append(_res)

    return all(self._enabled_modules)

  import_many = _import_multiple_modules
  require_many = _import_multiple_modules

  @CacheMethod(maxsize=None)
  def _import_single_module(self, *args, **kwargs):
    """"Import module in global context with self reference.

      @update import module in global context and provide as attribute or accessible as sys.modules

      @ToDo: Multiple instances of a module

      @usage
      require_global(module_name, import_as, alternate_if_not_available)

      :param module|0: (str)
      :param as|1: (str|None)
      :param alternate|2: (str|None)

      :return: True: if module/alternate is imported
      :return: False: If no module could be imported
    """
    _module = kwargs.get("module", args[0] if len(args) > 0 else None)
    _as = kwargs.get("as", args[1] if len(args) > 1 else None)
    _alternate = kwargs.get("alternate", args[2] if len(args) > 2 else False)

    if _as is None:
      _as = _module

    if hasattr(self, _as) and getattr(self, _as, None) is not None:
      hasattr(self, 'log_debug') and self.log_debug(f"BASE_01: Module {_module} as {_as} already imported.")
      return True

    _module_instance = None
    if _module in self.SYS.modules.keys():
      hasattr(self, 'log_debug') and  self.log_debug(f"BASE_02: {_module} as {_as} referred from global context.")
      _module_instance = self.SYS.modules[_module]
    else:
      try:
        __i = MODULE_IMPORTER.import_module(_module)
        hasattr(self, 'log_debug') and  self.log_debug(f"BASE_03: Imported {_module}")
        _module_instance = __i
      except:
        self.log_error(f"`{_module} as {_as}` could not be imported.")
        try:
          hasattr(self, 'log_debug') and  self.log_debug(f"BASE_04: {_module} could not be imported. Trying to import {_alternate}.")
          if _alternate and isinstance(_alternate, (str)):
            __i = MODULE_IMPORTER.import_module(_alternate)
            _module_instance = __i
        except:
          _error_message = f"{_module} as {_as} or its alternate {_alternate} could not be imported."
          self.log_error(_error_message)

    if _module_instance is None:
      return False

    # To understand most imported modules
    self._imported_modules.append((_as, ))
    setattr(self, _as, _module_instance)
    return True

  import_module = _import_single_module
  require = _import_single_module
  require_global = _import_single_module

  def _extract_py_classes(self, *args, **kwargs):
    _path_file = kwargs.get('path_file', args[0] if len(args) > 0 else None)
    _path_file = EntityPath(_path_file)
    _classes = []
    if _path_file.is_file():
      self.require('ast', 'PyAST')
      _tree = self.PyAST.parse(_path_file.read())
      _classes = [_n.name for _n in self.PyAST.walk(_tree) if isinstance(_n, self.PyAST.ClassDef)]

    return _classes

  def _py_class_refs(self, *args, **kwargs):
    _path_file = kwargs.get('path_file', args[0] if len(args) > 0 else None)
    _path_file = EntityPath(_path_file)
    _classname = kwargs.get('classname', args[1] if len(args) > 1 else _path_file.stem)
    if _path_file.is_file():
      import importlib.util as ILUtil
      _mod_name = _path_file.stem
      _spec = ILUtil.spec_from_file_location(_mod_name, _path_file)
      _module = ILUtil.module_from_spec(_spec)
      self.SYS.modules[_mod_name] = _module
      _spec.loader.exec_module(_module)
      return getattr(_module, _classname)

  def list_py_classes(self, *args, **kwargs):
    """Lists classes as {class:filename...} pair
    """
    _path = kwargs.get('path', args[0] if len(args) > 0 else EntityPath())
    _path = EntityPath(_path)
    _flag_ref = kwargs.get('flag_ref', False)

    _pattern_file = "*.py"
    if _path.is_file():
      _pattern_file = f"{_path.stem}*.py"
      _path = _path.parent()

    _classes = {}
    for _file in _path.search(_pattern_file):
      _cl = self._extract_py_classes(_file)
      if _flag_ref is False:
        _classes[_file.stem] = _cl
      else:
        _classes[_file.stem] = [self._py_class_refs(_file, _p) for _p in _cl]

    return _classes
