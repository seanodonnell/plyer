'''
Linux GPS via UbuntuGeoIP
-----------
'''
import warnings
from kivy.clock import Clock
from plyer.facades import GPS


class DBusGPS(GPS):

    def _configure(self):
        import dbus
        bus = dbus.SessionBus()
        self.geoclue = bus.get_object(
            'org.freedesktop.Geoclue.Providers.UbuntuGeoIP',
            '/org/freedesktop/Geoclue/Providers/UbuntuGeoIP')

    def _start(self, **kwargs):
        # update location once a minute, given its resolved by
        # ip only changing network changes location information
        self.location_event = Clock.schedule_interval(self._get_location, 5)

    def _get_location(self, dt):
        # note to self, just get this to return the same location to start
        # with every 60 seconds, then worry about dbus after

        position_info = self.geoclue.GetPosition(
            dbus_interface='org.freedesktop.Geoclue.Position')

        self.on_location(lat=position_info[2], lon=position_info[3])

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
