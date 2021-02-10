"""Config flow for local weather rss."""
import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import (CONF_SCAN_INTERVAL)

from .const import DOMAIN

CONF_NAME    = 'name'
CONF_LOCAL_CODE = 'localcode'
CONF_PROP    = 'properties'

default_name = 'local_weather_rss'

_LOGGER = logging.getLogger(__name__)

class localWeatherRssConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for local weather rss."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize flow."""
        self._localcode: Required[str] = None
        self._name: Optional[str]      = "local_weather_rss"
        self._properties: Optional[bool] = False

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            self._localcode     = user_input[CONF_LOCAL_CODE]
            self._name          = user_input[CONF_NAME]
            self._properties    = user_input[CONF_PROP]

            return self.async_create_entry(title=DOMAIN, data=user_input)

        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is None:
            return self._show_user_form(errors)

    async def async_step_import(self, import_info):
        """Handle import from config file."""
        return await self.async_step_user(import_info)

    @callback
    def _show_user_form(self, errors=None):
        schema = vol.Schema(
            {
                vol.Optional(CONF_NAME, default=default_name): str,
                vol.Required(CONF_LOCAL_CODE): str,
                vol.Optional(CONF_PROP, default=False): bool,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors or {}
        )
