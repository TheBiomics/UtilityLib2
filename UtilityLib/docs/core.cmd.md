class CommandUtility(UtilityLib.core.log.LoggingUtility)
  CommandUtility(*args, **kwargs)

  ## MRO:
      CommandUtility
      UtilityLib.core.log.LoggingUtility
      UtilityLib.core.time.TimeUtility
      UtilityLib.BaseUtility
      builtins.object

  ## Methods:

  __enter__(self)

  __exit__(self, *args, **kwargs)

  __init__(self, *args, **kwargs)
      Initialize self.  See help(type(self)) for accurate signature.

  call_cmd = cmd_call(self, *args, **kwargs)

  call_command = cmd_call(self, *args, **kwargs)

  cmd_call(self, *args, **kwargs)
      Call a command without capturing output.

      :param command: The command to run.
      :return: The return code of the command.

  cmd_call_echo = cmd_run_mock(self, *args, **kwargs)

  cmd_call_mock = cmd_run_mock(self, *args, **kwargs)

  cmd_dry_run = cmd_run_mock(self, *args, **kwargs)

  cmd_is_exe = is_executable(self, program)

  cmd_run(self, *args, **kwargs)
      Run a command and capture the output.

      :param command: The command to run.
      :param newlines: Whether to treat the output as text with newlines.
      :return: The output of the command.

  cmd_run_mock(self, *args, **kwargs)
      Mocks cmd_run/cmd_call

  cmd_which(self, program)

  contextual_directory(self, new_path)
      A context manager for changing the current working directory
      later switches back to the original directory.

  flatten_args(self, *args, **kwargs)

  get_cli_args(self, *args, **kwargs)
      @example

      _cli_settings = {
        ...
        "db_path": (['-db'], None, None, 'Provide path to the database for Sieve project.', {}),
        "path_base": (['-b'], "*", [OS.getcwd()], 'Provide base directory to run the process.', {}),
        ...
      }

  guess_nargs_from_default(self, *args, **kwargs)

  init_cli(self, *args, **kwargs)

  init_multiprocessing(self, *args, **kwargs)

  is_exe = is_executable(self, program)

  is_executable(self, program)

  process_queue(self, *args, **kwargs)
      Process tasks from the queue

  queue_final_callback(self, callback=None, *args, **kwargs) -> None

  queue_task(self, func, *args, **kwargs) -> None
      Queue a function operation

      @example:
      def method_to_execute(self, *arg, **kwargs):
        return arg ** 2

      _.init_multiprocessing
      _.queue_task(method_to_execute, *args, **kwargs)
      _.process_queue
      _.queue_final_callback

  queue_timed_callback(self, callback=None, *args, **kwargs) -> None

  run_cmd = cmd_run(self, *args, **kwargs)

  run_command = cmd_run(self, *args, **kwargs)

  start_mp = init_multiprocessing(self, *args, **kwargs)

  sys_open_files(self)
      Returns list of open files or open file handles by system

  unregistered_arg_parser(self, *args, **kwargs)
      Processes uregistered arguments from commandline

      @accepts
      List/Tuple

      @return
      dict() with/out values

  which = cmd_which(self, program)

  ----------------------------------------------------------------------
  ## ReadOnlyProperties:

  queue_done

  queue_failed
      Blocking

  queue_pending

  queue_running
      Blocking

  queue_task_status

  ----------------------------------------------------------------------
  ## Attributes:

  future_objects = []

  max_workers = 32

  num_cores = 8

  semaphore = None

  task_queue = None

  thread_pool = None
