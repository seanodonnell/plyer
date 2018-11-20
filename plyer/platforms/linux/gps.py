'''
Linux GPS via UbuntuGeoIP
-----------
'''
import warnings
from kivy.clock import Clock
from plyer.facades import GPS


class DBusGPS(GPS):

    def _configure(self):
        pass

    def _start(self, **kwargs):
        # update location once a minute, given its resolved by
        # ip only changing network changes location information
        self.location_event = Clock.schedule_interval(self._get_location, 5)

    def _get_location(self, dt):
        # note to self, just get this to return the same location to start
        # with every 60 seconds, then worry about dbus after
        self.on_location(lat=1, lon=1)

    def _stop(self):
        Clock.unschedule(self.location_event)


def instance():
    try:
        import dbus  # pylint: disable=unused-variable
        return DBusGPS()
    except ImportError:
        msg = ("The Python dbus package is not installed.\n"
               "Try installing it with your distribution's package manager, "
               "it is usually called python-dbus or python3-dbus, but you "
               "might have to try dbus-python instead, e.g. when using pip.")
        warnings.warn(msg)
