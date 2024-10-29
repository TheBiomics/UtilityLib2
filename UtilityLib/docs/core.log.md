Help on class LoggingUtility in module UtilityLib.core.log:

class LoggingUtility(UtilityLib.core.time.TimeUtility)
  LoggingUtility(*args, **kwargs)

  ## MRO:
      LoggingUtility
      UtilityLib.core.time.TimeUtility
      UtilityLib.BaseUtility
      builtins.object

  ## Methods:

  __init__(self, *args, **kwargs)

  debug = log_debug(self, *args, **kwargs)

  emergency = log_critical(self, *args, **kwargs)

  error = log_error(self, *args, **kwargs)

  error_traceback(self, _error)

  info = log_info(self, *args, **kwargs)

  log = _log(self, *args, **kwargs) -> None

  log_critical(self, *args, **kwargs)

  log_debug(self, *args, **kwargs)

  log_error(self, *args, **kwargs)

  log_fail = log_critical(self, *args, **kwargs)

  log_info(self, *args, **kwargs)

  log_success = log_info(self, *args, **kwargs)

  log_warning(self, *args, **kwargs)

  report = _log(self, *args, **kwargs) -> None

  set_logging(self, *args, **kwargs)
      Logging Setup

  warning = log_warning(self, *args, **kwargs)

  ----------------------------------------------------------------------
  ## Attributes:

  LogHandler = None

  log_file_name = 'UtilityLib.log'

  log_file_path = None

  log_level = 10

  log_to_console = True

  log_to_file = True

  log_type = 'info'
