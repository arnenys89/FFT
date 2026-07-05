import logging
from collections import deque
import numpy as np
from scipy.fft import fft
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo

_LOGGER = logging.getLogger(__name__)

class FFTSensor(SensorEntity):
    def __init__(self, hass, sensor_id, buffer_size, name):
        self.hass = hass
        self._sensor_id = sensor_id
        self._buffer_size = buffer_size
        self._name = name
        self._buffer = deque(maxlen=buffer_size)
        self._state = None
        self._attr_name = name
        self._attr_unique_id = f"fft_sensor_{sensor_id}"

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
