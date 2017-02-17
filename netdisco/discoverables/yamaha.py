"""Discover Yamaha Receivers."""
from . import SSDPDiscoverable


class Discoverable(SSDPDiscoverable):
    """Add support for discovering Yamaha Receivers."""

    REMOTE_CONTROL_SPEC_TYPE =\
        'urn:schemas-yamaha-com:service:X_YamahaRemoteControl:1'

    def info_from_entry(self, entry):
        """Return the most important info from a uPnP entry."""
        yam = entry.description['X_device']
        services = yam['X_serviceList']['X_service']
        if isinstance(services, list):
            service = next(
                (s for s in services
                 if s['X_specType'] == self.REMOTE_CONTROL_SPEC_TYPE),
                services[0])
        else:
            service = services
        # do a slice of the second element so we don't have double /
        ctrlurl = (yam['X_URLBase'] + service['X_controlURL'][1:])
        descurl = (yam['X_URLBase'] + service['X_unitDescURL'][1:])
        device = entry.description['device']

        return (device['friendlyName'], device['modelName'], ctrlurl, descurl)

    def get_entries(self):
        """Get all the Yamaha uPnP entries."""
        return self.find_by_device_description({
            "manufacturer": "Yamaha Corporation",
            "deviceType": "urn:schemas-upnp-org:device:MediaRenderer:1"
        })
