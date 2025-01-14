from .base import BaseUtility
from ..lib.time import EntityTime

class TimeUtility(BaseUtility):
  DeltaTime = EntityTime.DeltaTime
  def __init__(self, *args, **kwargs):
    __defaults = {
        "duration": 3,
      }
    __defaults.update(kwargs)
    super().__init__(**__defaults)
    self.time_start()

  @property
  def datetime(self):
    """Time format: 12:54:54"""
    return EntityTime()

  @property
  def deltatime(self):
    """Time format: 12:54:54"""
    return EntityTime().DeltaTime

  @property
  def time(self):
    """Time format: 12:54:54"""
    return str(EntityTime().time)[:-7]

  @property
  def time_ms(self):
    """Time format: 12:54:54.111"""
    return str(EntityTime().time)[:-3]

  @property
  def time_us(self):
    """Time format: 12:54:54.111111"""
    return str(EntityTime().time)

  @property
  def date(self):
    """Date format: 2024-10-24"""
    return str(EntityTime().date)

  @property
  def day(self):
    return self.datetime._datetime.day

  @property
  def weekday(self):
    return self.datetime._datetime.strftime("%A")

  day_name = weekday

  @property
  def month(self):
    return self.datetime._datetime.month

  @property
  def month_name(self):
    return self.datetime._datetime.strftime('%B')

  @property
  def year(self):
    return self.datetime._datetime.year

  @property
  def hour(self):
    return self.datetime._datetime.hour

  @property
  def minute(self):
    return self.datetime._datetime.minute

  @property
  def second(self):
    return self.datetime._datetime.second

  @property
  def ts_us(self):
    """Timestamp with microseconds e.g., 1729927233.803901"""
    return EntityTime().timestamp

  @property
  def time_stamp(self):
    """Timestamp rounded off e.g., 1729927233"""
    return int(self.ts_us)

  timestamp = time_stamp

  def time_string(self, *args, **kwargs):
    # https://stackoverflow.com/a/10981895/6213452
    _timestamp = args[0] if len(args) > 0 else kwargs.get("timestamp", self.time_get())
    return EntityTime(_timestamp, **kwargs).string

  def time_elapsed(self, *args, **kwargs):
    _from = args[0] if len(args) > 0 else kwargs.get("from", self.time_get())
    _human_readable = args[1] if len(args) > 1 else kwargs.get("human_readable", False)
    _seconds_elapsed = _from - self.start_time

    _time_delta = EntityTime.DeltaTime.timedelta(seconds=_seconds_elapsed)
    _res_time = str(_time_delta)

    if _human_readable:
      _res_time = self.time_string(_time_delta)

    return _res_time

  def time_get(self, *args, **kwargs):
    self.pinned_time = EntityTime(**kwargs).timestamp
    return self.pinned_time

  def time_start(self, *args, **kwargs):
    self.start_time = self.time_get()
    self.pinned_time = self.time_get()
    return self.start_time

  def time_end(self, *args, **kwargs):
    return self.time_get() - self.start_time

  def _sleep(self, *args, **kwargs):
    """Sleep for certain `duration|0` in seconds."""
    self.update_attributes(self, kwargs)
    self.duration = kwargs.get("duration", args[0] if len(args) > 0 else getattr(self, "duration"))
    self.require("time", "TIME")
    return self.TIME.sleep(self.duration)

  sleep = _sleep
  wait = _sleep
  time_break = _sleep
  time_pause = _sleep
  time_sleep = _sleep

  def sleep_ms(self, *args, **kwargs):
    """Sleep for certain `duration|0` in milliseconds."""
    self.duration = kwargs.get("duration", args[0] if len(args) > 0 else getattr(self, "duration"))
    kwargs['duration'] = float(self.duration) / 1000
    return self._sleep(*args, **kwargs)

  def sleep_random(self, *args, **kwargs):
    """Sleep for random seconds between `min|0` and `max|1`."""
    _min = kwargs.get("min", args[0] if len(args) > 0 else 0)
    _max = kwargs.get("max", args[1] if len(args) > 1 else 6)

    self.require("random", "RANDOM")
    _duration = self.RANDOM.uniform(float(_min), float(_max))
    kwargs['duration'] = _duration
    return self._sleep(**kwargs)
