from functools import lru_cache as CacheMethod
from contextlib import contextmanager
from ..lib.obj import ObjDict
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
      _command.append(f"{_key}")
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
    _cwd = kwargs.pop('cwd', None)
    _command = self._format_command(*args, **kwargs)
    _command_str = ' '.join(_command)

    self.require('subprocess', 'SubProcess')
    try:
      self.log_debug(f"CMD_007: Calling command: {_command_str}")
      _result = self.SubProcess.call(_command, cwd=_cwd)
      return _result
    except Exception as _e:
      self.log_error(f"Command '{_command_str}' failed with error: {_e}")
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

    self.require('subprocess', 'SubProcess')

    _cmd_params = kwargs.pop('cmd_params', {
          "universal_newlines": kwargs.pop('newlines', True),
          "cwd": kwargs.pop('cwd', None),
          "check": kwargs.pop('check', None),
          "shell": kwargs.pop('shell', None),
          "capture_output": kwargs.pop('text', True),
          "text": kwargs.pop('text', None),
        })

    if not isinstance(_cmd_params, (dict)):
      _cmd_params = dict()
    else:
      _cmd_params = {_k: _v for _k, _v in _cmd_params.items() if _v is not None}

    _command = self._format_command(*args, **kwargs)
    _command_str = ' '.join(_command)

    try:
      self.log_debug(f"CMD_008: Running command: {_command_str}")
      _result = self.SubProcess.run(_command, **_cmd_params)
      self.log_debug(f"CMD_009: Command output: {_result.stdout}")
      return _result.stdout
    except self.SubProcess.CalledProcessError as _e:
      self.log_error(f"Command '{_command_str}' failed with error: {_e.stderr}")
      return None

  run_command = cmd_run
  run_cmd = cmd_run

  def cmd_run_mock(self, *args, **kwargs):
    """Mocks cmd_run/cmd_call"""
    return self.cmd_run('echo', *args, **kwargs)

  cmd_dry_run = cmd_run_mock
  cmd_call_mock = cmd_run_mock
  cmd_call_echo = cmd_run_mock

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
  max_workers = 32
  num_cores = 8
  thread_pool = None
  semaphore = None
  task_queue = None
  future_objects = []

  def _get_max_workers(self):
    # Get the number of CPU cores available
    self.num_cores = min(self.OS.cpu_count(), self.num_cores)
    # Adjust max_workers based on available CPU cores and workload
    self.max_workers = min(2 * self.num_cores, self.max_workers)  # Example: Limit to 2x CPU cores or 32 workers, whichever is lower
    return self.max_workers

  def init_multiprocessing(self, *args, **kwargs):
    self.update_attributes(self, kwargs)
    self.require('concurrent.futures', 'ConcurrentFutures')
    self.require('threading', 'Threading')
    self.require('queue', 'QueueProvider')
    self._get_max_workers()
    self.task_queue = self.QueueProvider.Queue()
    self.semaphore = self.Threading.Semaphore(self.max_workers - 1)
    self.thread_pool = self.ConcurrentFutures.ThreadPoolExecutor(max_workers=self.max_workers)
    self.log_debug(f"CMD_002:Starting with cores {self.num_cores} and max_workers {self.max_workers}.")

  start_mp = init_multiprocessing

  def __enter__(self):
    self.log_debug('CMD_004: Init multiprocessing.')
    self.init_multiprocessing()
    return self

  def __exit__(self, *args, **kwargs):
    self.log_debug('CMD_001: Shutting down the thread executor.')
    self.thread_pool.shutdown()

  @CacheMethod(maxsize=None)
  def _cache_wrapper(self, func, *arg, **kwarg):
    return func(*arg, **kwarg)

  def queue_task(self, func, *args, **kwargs) -> None:
    """Queue a function operation

@example:
def method_to_execute(self, *arg, **kwargs):
  # Example function to be cached
  return arg ** 2

_.init_multiprocessing
_.queue_task(method_to_execute, *args, **kwargs)
_.process_queue
_.queue_final_callback

"""
    self.task_queue.put((func, args, kwargs))

  def queue_timed_callback(self, callback=None, *args, **kwargs) -> None:
    _cb_interval = kwargs.pop("cb_interval", 300)
    if not callback is None and callable(callback):
      self.require('threading', 'Threading')
      self.log_debug(f'CMD_003: Delegating a callback in {_cb_interval}s.')
      self.Threading.Timer(_cb_interval, callback, args=args, kwargs=kwargs)

  _queue_schedule_ref = None
  def queue_final_callback(self, callback=None, *args, **kwargs) -> None:
    if callback is not None and callable(callback):
      from ..lib.schedule import ScheduleEvent
      _cb_interval = kwargs.pop("cb_interval", 60)
      self._queue_schedule_ref = ScheduleEvent(func=self._queue_final_cb_fn_bg_exe, interval=_cb_interval, args=(callback, *args), **kwargs)

  def _queue_final_cb_fn_bg_exe(self, callback, *args, **kwargs) -> None:
    _job_t, _job_d = self.queue_task_status.total, self.queue_task_status.done
    if any([_job_d < _job_t, not self.task_queue.empty()]):
      self.log_debug(f'CMD_004: Job Status: {_job_t-_job_d}/{_job_t} to be done. ~zZ')
    elif self._queue_schedule_ref is not None:
      self.log_debug(f'CMD_005: Job Status: All {self.queue_done} job(s) completed. Executing final callback...')
      callback(*args, **kwargs)
      self._queue_schedule_ref.stop()

  def process_queue(self, *args, **kwargs):
    """Process tasks from the queue
      # Acquire semaphore to limit concurrency
      # Get task from the queue
      # Submit task to the executor
    """

    while not self.task_queue.empty():
      try:
        with self.semaphore:
          _func, _args, _kwargs = self.task_queue.get()
          _ftr_obj = self.thread_pool.submit(_func, *_args, **_kwargs)
          self.future_objects.append(_ftr_obj)
      except Exception as e:
        self.log_error(f"Error processing the queue: {e}")

    self._shut_down_queue(*args, **kwargs)
    return True

  def _shut_down_queue(self, *args, **kwargs):
    _wait = kwargs.get("wait", args[0] if len(args) > 0 else False)
    self.log_debug(f'CMD_006: Setting queue wait = {_wait}.')

    if _wait:
      # Wait for all tasks to complete
      self.ConcurrentFutures.wait(self.future_objects)

    # Shutdown the ThreadPoolExecutor
    self.thread_pool.shutdown(wait=_wait)

  @property
  def queue_running(self) -> int:
    """Blocking"""
    return sum(map(lambda _fo: bool(_fo.running()), self.ConcurrentFutures.as_completed(self.future_objects)))

  @property
  def queue_failed(self) -> int:
    """Blocking"""
    return sum(map(lambda _fo: bool(_fo.exception()), self.ConcurrentFutures.as_completed(self.future_objects)))

  @property
  def queue_done(self) -> int:
    return self.queue_task_status.done

  @property
  def queue_pending(self) -> int:
    return self.queue_task_status.pending

  @property
  def queue_task_status(self) -> dict:
    _total = len(self.future_objects)
    _done = sum(map(lambda _fo: bool(_fo.done()), self.future_objects))

    return ObjDict({
      "total": _total,
      "done": _done,
      "pending": _total - _done, # _fo.done() - _fo.running()
    })

  def sys_open_files(self):
    """Returns list of open files or open file handles by system"""
    import psutil as PC
    _p = PC.Process()
    return _p.open_files()

  @contextmanager
  def contextual_directory(self, new_path):
    """A context manager for changing the current working directory
    later switches back to the original directory.

    """
    _old_path = self.OS.getcwd()
    try:
      self.OS.chdir(new_path)
      yield
    finally:
      self.OS.chdir(_old_path)
