"""Local Weather RSS Sensor for Home Assistant"""
import voluptuous as vol

from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import CONF_NAME, CONF_MONITORED_CONDITIONS
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, PLATFORM

CONF_LOCAL_CODE = 'localcode'
CONF_PROP       = 'properties'

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.All(
            vol.Schema({vol.Optional(CONF_NAME, default=DOMAIN): cv.string}),
            vol.Schema({vol.Required(CONF_LOCAL_CODE): cv.string}),
            vol.Schema({vol.Optional(CONF_PROP, default=False): cv.boolean}),
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up local_ip from configuration.yaml."""
    conf = config.get(DOMAIN)
#    if conf:
#        hass.async_create_task(
#            hass.config_entries.flow.async_init(
#                DOMAIN, data=conf, context={"source": SOURCE_IMPORT}
#            )
#        )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up kweather from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORM)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    return await hass.config_entries.async_forward_entry_unload(entry, PLATFORM)
