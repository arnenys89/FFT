import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
import homeassistant.helpers.config_validation as cv

DOMAIN = "fft_sensor"

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="FFT Sensor", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("sensor_id"): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
                vol.Required("buffer_size", default=64): int,
                vol.Required("sample_rate", default=10): vol.Coerce(float),
                vol.Required("frequency_resolution", default=1): vol.Coerce(float),
                vol.Required("name", default="FFT Sensor"): str,
            }),
        )
