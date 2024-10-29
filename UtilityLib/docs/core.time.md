Help on class TimeUtility in module UtilityLib.core.time:

class TimeUtility(UtilityLib.BaseUtility)
  TimeUtility(*args, **kwargs)

  ## MRO:
      TimeUtility
      UtilityLib.BaseUtility
      builtins.object

  ## Methods:

  __init__(self, *args, **kwargs)

  sleep = _sleep(self, *args, **kwargs)

  sleep_ms(self, *args, **kwargs)
      Sleep for certain `duration|0` in milliseconds.

  sleep_random(self, *args, **kwargs)
      Sleep for random seconds between `min|0` and `max|1`.

  time_break = _sleep(self, *args, **kwargs)

  time_elapsed(self, *args, **kwargs)

  time_end(self, *args, **kwargs)

  time_get(self, *args, **kwargs)

  time_pause = _sleep(self, *args, **kwargs)

  time_sleep = _sleep(self, *args, **kwargs)

  time_start(self, *args, **kwargs)

  time_string(self, *args, **kwargs)

  wait = _sleep(self, *args, **kwargs)

  ----------------------------------------------------------------------
  ## ReadOnlyProperties:

  date
      Date format: 2024-10-24

  datetime
      Time format: 12:54:54

  day

  day_name

  deltatime
      Time format: 12:54:54

  hour

  minute

  month

  month_name

  second

  time
      Time format: 12:54:54

  time_ms
      Time format: 12:54:54.111

  time_stamp
      Timestamp rounded off e.g., 1729927233

  time_us
      Time format: 12:54:54.111111

  timestamp
      Timestamp rounded off e.g., 1729927233

  ts_us
      Timestamp with microseconds e.g., 1729927233.803901

  weekday

  year
