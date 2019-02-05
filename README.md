# timers
timer for python (decorator function and with class)

## Usage
```
import timers

"""with format."""
with timers.Timer():
    """Proc to measure time"""
    pass

"""decorator function."""
@timer.timer
def func():
    """some process..."""
    return
```
