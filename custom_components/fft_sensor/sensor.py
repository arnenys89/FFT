import logging
from collections import deque
import numpy as np
from scipy.fft import fft
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the FFT sensor platform."""
    async_add_entities([FFTSensor(hass, config_entry.data)])

class FFTSensor(SensorEntity):
    def __init__(self, hass, config):
        self.hass = hass
        self._sensor_id = config["sensor_id"]
        self._buffer_size = config["buffer_size"]
        self._sample_rate = config["sample_rate"]
        self._frequency_resolution = config["frequency_resolution"]
        self._name = config["name"]
        self._buffer = deque(maxlen=self._buffer_size)
        self._state = None
        self._attr_name = self._name
        self._attr_unique_id = f"fft_sensor_{self._sensor_id}"

    async def async_added_to_hass(self):
        self.hass.helpers.event.async_track_state_change(
            self._sensor_id, self._handle_state_change
        )

    def _handle_state_change(self, entity_id, old_state, new_state):
        if new_state is not None and new_state.state != "unknown":
            try:
                val = float(new_state.state)
                self._buffer.append(val)
                self._update_fft()
            except ValueError:
                pass

    def _update_fft(self):
        if len(self._buffer) == self._buffer_size:
            # Perform FFT
            data = np.array(self._buffer)
            # Use sample_rate if needed in advanced FFT logic,
            # but for now keep it simple as requested.
            fft_result = fft(data)
            # Take absolute value (magnitude spectrum)
            magnitude = np.abs(fft_result)
            # Simple result: mean of magnitude excluding DC component
            self._state = round(float(np.mean(magnitude[1:])), 2)
            self.async_write_ha_state()

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return "Hz"
