from functools import lru_cache as CacheMethod
from .log import LoggingUtility

class CommandUtility(LoggingUtility):
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

  def is_executable(self, program):
    return self.cmd_which(program) is not None

  cmd_is_exe = is_executable
  is_exe = is_executable

  def cmd_which(self, program):
    return self.SHUTIL.which(program)

  which = cmd_which

  def _format_command(self, *args, **kwargs):
    """
    Format the command with positional and keyword arguments.

    :param args: Positional arguments.
    :param kwargs: Keyword arguments.

    :return: List of command parts.
    """
    _command = list(args)

    for _key, _value in kwargs.items():
      _command.append(f"-{_key}")
      if isinstance(_value, (list, tuple, set)):
        _command.extend(list(_value))
      else:
        _command.append(_value)

    return list(map(str, _command))

  def cmd_call(self, *args, **kwargs):
    """
    Call a command without capturing output.

    :param command: The command to run.
    :return: The return code of the command.
    """
    _command = self._format_command(*args, **kwargs)

    self.require('subprocess', 'SubProcess')
    try:
      self.log_debug(f"Calling command: {_command}")
      _result = self.SubProcess.call(_command)
      return _result
    except Exception as _e:
      self.log_error(f"Command '{_command}' failed with error: {_e}")
      return None

  call_command = cmd_call
  call_cmd = cmd_call

  def cmd_run(self, *args, **kwargs):
    """
    Run a command and capture the output.

    :param command: The command to run.
    :param newlines: Whether to treat the output as text with newlines.
    :return: The output of the command.
    """

    _newlines = kwargs.pop('newlines', True)
    _command = self._format_command(*args, **kwargs)

    self.require('subprocess', 'SubProcess')

    try:
      self.log_debug(f"Running command: {_command}")
      _result = self.SubProcess.run(
          _command,
          stdout=self.SubProcess.PIPE,
          stderr=self.SubProcess.PIPE,
          universal_newlines=_newlines,
          check=True
      )
      self.log_debug(f"Command output: {_result.stdout}")
      return _result.stdout
    except self.SubProcess.CalledProcessError as _e:
      self.log_error(f"Command '{_command}' failed with error: {_e.stderr}")
      return None

  run_command = cmd_run
  run_cmd = cmd_run

  def flatten_args(self, *args, **kwargs):
    _args = args[0] if len(args) > 0 else kwargs.get("mapping", [])
    _flattened = {}
    if isinstance(_args, (dict)):
      _flattened = {_k: _v[0] if len(_v) == 1 else _v for _k, _v in _args.items()}
    return _flattened

  def unregistered_arg_parser(self, *args, **kwargs):
    """Processes uregistered arguments from commandline

      @accepts
      List/Tuple

      @return
      dict() with/out values
    """
    _un_args = args[0] if len(args) > 0 else kwargs.get("unregistered_args", [])

    _arg_aggregator = {}
    _key = None
    for _ua in _un_args:

      if _ua.startswith(("-", "--")):
        _key = _ua.strip("-")
        _key, _attached_value = _key.split("=", 1) if "=" in _key else (_key, "")

        if not _key in _arg_aggregator.keys():
          _arg_aggregator[_key] = []

        _arg_aggregator[_key].append(_attached_value) if len(_attached_value) > 0 else None

      elif _key and _key in _arg_aggregator.keys():
        _arg_aggregator[_key].append(_ua)

    return self.flatten_args(_arg_aggregator)

  def guess_nargs_from_default(self, *args, **kwargs):
    _default = args[0] if len(args) > 0 else kwargs.get("default")
    if _default is None:
      return None
    elif isinstance(_default, (str)):
      return "*"
    elif isinstance(_default, (list, tuple, set, dict)):
      return

  def init_cli(self, *args, **kwargs):
    self.require('argparse', 'ArgParser')

    _version = args[0] if len(args) > 0 else kwargs.get("version", "unknown")
    self.cmd_arg_parser = self.ArgParser.ArgumentParser(prog=_version)
    self.cmd_arg_parser.add_argument('-v', '--version', action='version', version=_version)

  def get_cli_args(self, *args, **kwargs):
    """
      @example

      _cli_settings = {
        ...
        "db_path": (['-db'], None, None, 'Provide path to the database for Sieve project.', {}),
        "path_base": (['-b'], "*", [OS.getcwd()], 'Provide base directory to run the process.', {}),
        ...
      }
    """

    if not hasattr(self, "cmd_arg_parser"):
      self.init_cli(**kwargs)

    _cli_args = args[0] if len(args) > 0 else kwargs.get("cli_args", {})

    for _arg_key, _arg_value in _cli_args.items():

      _keys = _arg_value[0]
      _keys.append(f"--{_arg_key}")

      _keys = [_k if "-" in _k else f"-{_k}" for _k in _keys] # Add atleast one - to the argument identifier

      _cmd_keys = _arg_value[0]
      _nargs = _arg_value[1]
      _default = _arg_value[2]
      _help = _arg_value[3]

      if not '%(default)s' in _help:
        _help = f"{_help} (Default: %(default)s)"

      _kws = _arg_value[4]
      _kws.update({
        "nargs": _nargs,
        "default": _default,
        "help": _help,
      })

      self.cmd_arg_parser.add_argument(*list(_cmd_keys), **_kws)

    _reg_args, _unreg_args = self.cmd_arg_parser.parse_known_args()
    _reg_args = vars(_reg_args)
    _params = self.unregistered_arg_parser(_unreg_args)
    _params.update(_reg_args)
    return _params

  # Multithreading
  max_workers = None
  thread_executor = None
  semaphore = None
  task_queue = None
  future_objects = []

  def _get_max_workers(self):
    # Get the number of CPU cores available
    _num_cores = self.OS.cpu_count()
    # Adjust max_workers based on available CPU cores and workload
    self.max_workers = min(2 * _num_cores, 32)  # Example: Limit to 2x CPU cores or 32 workers, whichever is lower
    return self.max_workers

  def init_multiprocessing(self):
    self.require('concurrent.futures', 'ConcurrentTasks')
    self.require('threading', 'Threading')
    self.require('queue', 'QueueProvider')
    self._get_max_workers()
    self.task_queue = self.QueueProvider.Queue()
    self.semaphore = self.Threading.Semaphore(self.max_workers)
    self.thread_executor = self.ConcurrentTasks.ThreadPoolExecutor(max_workers=self.max_workers)

  def __enter__(self):
    self.init_multiprocessing()
    return self

  def __exit__(self, *args, **kwargs):
    self.thread_executor.shutdown()

  @CacheMethod(maxsize=None)
  def _cache_wrapper(self, func, *arg, **kwarg):
    return func(*arg, **kwarg)

  def queue_task(self, func, *args, **kwargs):
    """Queue a function operation

@example:
def method_to_execute(self, *arg, **kwargs):
  # Example function to be cached
  return arg ** 2

_cu = CommandUtility()
_cu.init_multiprocessing()
_cu.queue_task(method_to_execute, *args, **kwargs)

"""
    self.task_queue.put((func, args, kwargs))

  def process_queue(self, wait=False):
    # Process tasks from the queue
    while not self.task_queue.empty():
      # Acquire semaphore to limit concurrency
      try:
        with self.semaphore:
          # Get task from the queue
          _func, _args, _kwargs = self.task_queue.get()
          # Submit task to the executor
          _ftr_obj = self.thread_executor.submit(_func, *_args, **_kwargs)
          self.future_objects.append(_ftr_obj)
      except Exception as e:
        # Handle exceptions raised during file operation
        print(f"Error processing the queue: {e}")

    if wait:
      self._wait_for_completion()

  def _wait_for_completion(self):
    # Wait for all tasks to complete
    self.ConcurrentTasks.wait(self.future_objects)
    # Shutdown the ThreadPoolExecutor
    self.thread_executor.shutdown(wait=True)

  def queue_task_status(self):
    # ToDo: ObjDict::config
    self.config.jobs.done = sum(1 for _ftr in self.future_objects if _ftr.done())
    self.config.jobs.pending = sum(1 for _ftr in self.future_objects if not _ftr.done() and not _ftr.running())
    self.config.jobs.running = sum(1 for _ftr in self.future_objects if not _ftr.done() and _ftr.running())
    return self.config.jobs

  def sys_open_files(self):
    import psutil as PC
    _p = PC.Process()
    return _p.open_files()
