"""Sensor platform for Subscription Helper integration."""

from __future__ import annotations

from datetime import date, timedelta

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.event import async_track_time_interval

from .const import (
    CONF_ACCOUNT_NUMBER,
    CONF_CANCELLATION_PERIOD,
    CONF_CONTRACT_LENGTH,
    CONF_COST,
    CONF_END_DATE,
    CONF_NOTES,
    CONF_PAYMENT_METHOD,
    CONF_PROVIDER,
    CONF_RENEWAL_PERIOD,
    CONF_SUBSCRIPTION_NAME,
    DOMAIN,
    EXPIRING_SOON_DAYS,
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Initialize Subscription Helper config entry."""
    name = config_entry.title
    unique_id = config_entry.entry_id

    async_add_entities(
        [
            SubscriptionDaysSensor(config_entry, name, unique_id),
            SubscriptionStatusSensor(config_entry, name, f"{unique_id}_status"),
        ]
    )


class SubscriptionDaysSensor(SensorEntity):
    """Sensor showing days until subscription ends."""

    _attr_has_entity_name = True
    _attr_translation_key = "days_remaining"
    _attr_native_unit_of_measurement = "days"
    _attr_icon = "mdi:calendar-clock"

    def __init__(self, config_entry: ConfigEntry, name: str, unique_id: str) -> None:
        """Initialize Subscription Days Sensor."""
        self._config_entry = config_entry
        self._attr_unique_id = f"{unique_id}_days"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, config_entry.entry_id)},
            "name": name,
        }
        self._update_state()

    @callback
    def _update_state(self) -> None:
        """Update the sensor state."""
        end_date_str = self._config_entry.options.get(
            CONF_END_DATE, self._config_entry.data.get(CONF_END_DATE)
        )

        if end_date_str:
            end_date = date.fromisoformat(end_date_str)
            today = date.today()
            days_remaining = (end_date - today).days
            self._attr_native_value = days_remaining
        else:
            self._attr_native_value = None

    async def async_added_to_hass(self) -> None:
        """Handle entity added to hass."""
        # Update daily at midnight
        self.async_on_remove(
            async_track_time_interval(
                self.hass, lambda _: self._update_state(), timedelta(hours=1)
            )
        )
        # Listen for config changes
        self._config_entry.async_on_unload(
            self._config_entry.add_update_listener(self._async_config_update)
        )

    async def _async_config_update(
        self, hass: HomeAssistant, entry: ConfigEntry
    ) -> None:
        """Handle config update."""
        self._update_state()
        self.async_write_ha_state()


class SubscriptionStatusSensor(SensorEntity):
    """Sensor showing subscription status."""

    _attr_has_entity_name = True
    _attr_translation_key = "status"
    _attr_icon = "mdi:information"
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = ["active", "expiring_soon", "expired"]

    def __init__(self, config_entry: ConfigEntry, name: str, unique_id: str) -> None:
        """Initialize Subscription Status Sensor."""
        self._config_entry = config_entry
        self._attr_unique_id = unique_id
        self._attr_device_info = {
            "identifiers": {(DOMAIN, config_entry.entry_id)},
            "name": name,
        }
        self._update_state()

    @callback
    def _update_state(self) -> None:
        """Update the sensor state."""
        end_date_str = self._config_entry.options.get(
            CONF_END_DATE, self._config_entry.data.get(CONF_END_DATE)
        )

        if end_date_str:
            end_date = date.fromisoformat(end_date_str)
            today = date.today()
            days_remaining = (end_date - today).days

            if days_remaining < 0:
                self._attr_native_value = "expired"
            elif days_remaining <= EXPIRING_SOON_DAYS:
                self._attr_native_value = "expiring_soon"
            else:
                self._attr_native_value = "active"
        else:
            self._attr_native_value = "active"

        # Add extra attributes
        cost = self._config_entry.options.get(
            CONF_COST, self._config_entry.data.get(CONF_COST)
        )
        renewal_period = self._config_entry.options.get(
            CONF_RENEWAL_PERIOD, self._config_entry.data.get(CONF_RENEWAL_PERIOD)
        )
        provider = self._config_entry.options.get(
            CONF_PROVIDER, self._config_entry.data.get(CONF_PROVIDER)
        )
        cancellation_period = self._config_entry.options.get(
            CONF_CANCELLATION_PERIOD,
            self._config_entry.data.get(CONF_CANCELLATION_PERIOD),
        )
        contract_length = self._config_entry.options.get(
            CONF_CONTRACT_LENGTH, self._config_entry.data.get(CONF_CONTRACT_LENGTH)
        )
        payment_method = self._config_entry.options.get(
            CONF_PAYMENT_METHOD, self._config_entry.data.get(CONF_PAYMENT_METHOD)
        )
        account_number = self._config_entry.options.get(
            CONF_ACCOUNT_NUMBER, self._config_entry.data.get(CONF_ACCOUNT_NUMBER)
        )
        notes = self._config_entry.options.get(
            CONF_NOTES, self._config_entry.data.get(CONF_NOTES)
        )

        self._attr_extra_state_attributes = {}
        if end_date_str:
            self._attr_extra_state_attributes["end_date"] = end_date_str
        if cost is not None:
            self._attr_extra_state_attributes["cost"] = cost
        if renewal_period:
            self._attr_extra_state_attributes["renewal_period"] = renewal_period
        if provider:
            self._attr_extra_state_attributes["provider"] = provider
        if cancellation_period is not None:
            self._attr_extra_state_attributes["cancellation_period"] = (
                cancellation_period
            )
        if contract_length is not None:
            self._attr_extra_state_attributes["contract_length"] = contract_length
        if payment_method:
            self._attr_extra_state_attributes["payment_method"] = payment_method
        if account_number:
            self._attr_extra_state_attributes["account_number"] = account_number
        if notes:
            self._attr_extra_state_attributes["notes"] = notes

    async def async_added_to_hass(self) -> None:
        """Handle entity added to hass."""
        # Update daily
        self.async_on_remove(
            async_track_time_interval(
                self.hass, lambda _: self._update_state(), timedelta(hours=1)
            )
        )
        # Listen for config changes
        self._config_entry.async_on_unload(
            self._config_entry.add_update_listener(self._async_config_update)
        )

    async def _async_config_update(
        self, hass: HomeAssistant, entry: ConfigEntry
    ) -> None:
        """Handle config update."""
        self._update_state()
        self.async_write_ha_state()
