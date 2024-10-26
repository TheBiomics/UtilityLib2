import threading
import time
import schedule

class ScheduleEvent:
  """
    ### Example
    def method_x(*args, **kwargs):
      print(args, kwargs)
    # Create a scheduled event for method_x to run every 5 minutes
    _sch_ev = ScheduleEvent(method_x, 5, 'seconds',
                    1, 2, 3, ..., 
                    kw1=1, kw2=2, ..., limit=9)
    # do_something
    _sch_ev.stop()
  """

  def __init__(self, *args, **kwargs):
    """
      Schedule a method to be run in background

      :param func|0: Function to be executed on schedule.
      :param interval|1: Frequency to check and execute scheduled jobs.
      :param unit|2: seconds, minutes, ...
      :param limit: Allowed iterations (999999)
    """
    args = [*args]
    _n_args = len(args)

    self.func = kwargs.pop('func', args.pop(0) if _n_args > 0 else print)
    self.interval = kwargs.pop('interval', args.pop(0) if _n_args > 1 else 5)
    self.unit = kwargs.pop('unit', args.pop(0) if _n_args > 2 else 'seconds')
    self.limit = kwargs.pop('limit', 999999)

    self.counter = 0
    self.stop_event = threading.Event()
    self._setup_job(*args, **kwargs)
    self._start_continuous_run()

  def _setup_job(self, *args, **kwargs):
    """Set up the scheduled job with provided frequency."""
    if self.interval and callable(self.func):
      getattr(schedule.every(self.interval), self.unit).do(self.func, *args, **kwargs)

  def _start_continuous_run(self):
    """Start the continuous job scheduling in a background thread."""
    self.schedule_thread = threading.Thread(target=self._run_continuously)
    self.schedule_thread.start()

  def _run_continuously(self):
    """Run pending jobs in the background continuously."""
    while not self.stop_event.is_set():
      schedule.run_pending()
      self.counter += 1
      time.sleep(self.interval)

      if self.counter > self.limit:
        self.stop()

  def stop(self):
    """Stop the scheduled job and the background thread."""
    self.stop_event.set()
