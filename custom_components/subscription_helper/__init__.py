"""The Subscription Helper integration."""

from __future__ import annotations

from datetime import date
import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ServiceValidationError
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR]

SERVICE_UPDATE_OPTIONS = "update_options"
SERVICE_UPDATE_OPTIONS_SCHEMA = vol.Schema({
    vol.Required("config_entry_id"): cv.string,
    vol.Optional("end_date"): cv.date,
    vol.Optional("cost"): vol.Coerce(float),
    vol.Optional("renewal_period"): vol.In(["none", "monthly", "yearly"]),
    vol.Optional("provider"): cv.string,
    vol.Optional("cancellation_period"): vol.Coerce(int),
    vol.Optional("contract_length"): vol.Coerce(int),
    vol.Optional("payment_method"): cv.string,
    vol.Optional("account_number"): cv.string,
    vol.Optional("notes"): cv.string,
})


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Subscription Helper from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(config_entry_update_listener))
    
    # Register service
    async def handle_update_options(call: ServiceCall) -> None:
        """Handle the update_options service call."""
        config_entry_id = call.data["config_entry_id"]
        
        # Get the config entry
        if not (config_entry := hass.config_entries.async_get_entry(config_entry_id)):
            raise ServiceValidationError(f"Config entry {config_entry_id} not found")
        
        if config_entry.domain != DOMAIN:
            raise ServiceValidationError(f"Config entry {config_entry_id} is not a Subscription Helper")
        
        # Prepare new options
        new_options = dict(config_entry.options)
        
        # Update with provided values
        for key in ["end_date", "cost", "renewal_period", "provider", "cancellation_period", 
                    "contract_length", "payment_method", "account_number", "notes"]:
            if key in call.data:
                value = call.data[key]
                # Convert date to string
                if isinstance(value, date):
                    value = value.isoformat()
                new_options[key] = value
        
        # Update the config entry
        hass.config_entries.async_update_entry(config_entry, options=new_options)
        
        _LOGGER.info("Updated options for %s: %s", config_entry.title, new_options)
    
    hass.services.async_register(
        DOMAIN,
        SERVICE_UPDATE_OPTIONS,
        handle_update_options,
        schema=SERVICE_UPDATE_OPTIONS_SCHEMA,
    )
    
    return True


async def config_entry_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update listener, called when the config entry options are changed."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Unregister service if this is the last config entry
    if len([e for e in hass.config_entries.async_entries(DOMAIN) if e.entry_id != entry.entry_id]) == 0:
        hass.services.async_remove(DOMAIN, SERVICE_UPDATE_OPTIONS)
    
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
