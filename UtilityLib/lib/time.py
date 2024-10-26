from datetime import datetime as _DT
import re as _Rx
import pandas as PD

class DeltaTime(PD.Timedelta):
  """
  * Extends Pandas.Timedelta for inclusive functionality from NP.timedelta64 and datetime.timedelta functionality
  * Nanosecond precision for time

  * Example

  Get total hours in fractions
    _deltatime = DeltaTime('5 hours')
    _deltatime / Deltatime('1 m') # to get value in minutes

  """
  def __init__(self, *args, **kwargs):
    super().__init__()


class EntityTime():
  """EntityTime: To manage time and provide acessary methods

  @ToDo
  Extend PD.Timestamp???
  """
  DeltaTime = DeltaTime
  format = '%Y%m%d%H%M%S'
  PDTS = PD.Timestamp

  def __init__(self, *args, **kwargs):
    self._datetime = _DT.now()
    self.format = kwargs.get('format', self.format)

    if len(args) == 1 and isinstance(args[0], EntityTime):
      raise ValueError('Cyclic call.')
    elif len(args) == 1 and isinstance(args[0], str):
      if _Rx.match(r'^([+-]\d+)\s+(hour|hours|minute|minutes|day|days)$', args[0]):
        self._apply_shift(args[0])
      elif "%" in args[0]:
        self.format = args[0]
      else:
        # Assume string is a datetime format
        try:
          self._datetime = _DT.strptime(args[0], self.format)
        except Exception as _e:
          raise _e
    elif len(args) == 1 and isinstance(args[0], (int, float)):
      self._datetime = _DT.fromtimestamp(args[0])
    elif len(args) >= 3:
      # Assume (year, month, day, seconds)
      self._datetime = _DT(args[0], args[1], args[2]) + DeltaTime(seconds=args[3] if len(args) > 3 else 0)

  @property
  def date(self):
    return self._datetime.date()

  @property
  def time(self):
    return self._datetime.time()

  @property
  def string(self):
    return str(self._datetime.ctime())

  def get_format(self, *args, **kwargs):
    return self._datetime.strftime(*args, **kwargs)

  def get_isoformat(self, *args, **kwargs):
    """
      'auto', 'hours', 'minutes', 'seconds', 'milliseconds' and 'microseconds'
      [sep] -> string in ISO 8601 format, YYYY-MM-DDT[HH[:MM[:SS[.mmm[uuu]]]]][+HH:MM].
      [timespec] -> string in ISO 8601 format, YYYY-MM-DDT[HH[:MM[:SS[.mmm[uuu]]]]][+HH:MM].
    """
    return self._datetime.isoformat(*args, **kwargs)

  @property
  def current(self):
    return EntityTime()

  @property
  def _ts(self):
    return self._datetime.timestamp()

  timestamp = _ts
  stamp = _ts
  ts = _ts

  def __call__(self, *args, **kwargs):
    return EntityTime(*args, **kwargs)

  def _apply_shift(self, time_shift: str = None):
    """Applies a time shift to the current datetime."""

    if time_shift is None:
      return

    _unit_match = _Rx.match(r'([+-]\d+)\s+(hour|hours|minute|minutes|day|days)', time_shift)

    if _unit_match:
      _time_val = int(_unit_match.group(1))
      _time_unit = _unit_match.group(2)

      if _time_unit in ['hour', 'hours']:
        delta = DeltaTime(hours=_time_val)
      elif _time_unit in ['minute', 'minutes']:
        delta = DeltaTime(minutes=_time_val)
      elif _time_unit in ['day', 'days']:
        delta = DeltaTime(days=_time_val)
      else:
        raise ValueError(f"Unsupported time unit '{_time_unit}'")
      self._datetime += delta

  def __sub__(self, other):
    """Calculate the difference between two EntityTime instances or between EntityTime and a string/timestamp."""
    if isinstance(other, (str, float, int)):
      other = EntityTime(other)
    return DeltaTime(self._datetime - other._datetime)

  def __rsub__(self, other):
    """Reverse subtraction to handle EntityTime - string/timestamp cases.
    """
    if isinstance(other, (str, float, int)):
      other = EntityTime(other)
    return DeltaTime(other._datetime - self._datetime)

  def __iter__(self):
    return [self._datetime]

  def __repr__(self):
    return f"{self.string}"

  def __str__(self):
    return f"{self.string}"
