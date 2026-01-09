"""Config flow for the Subscription Helper integration."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, cast

import voluptuous as vol

from homeassistant.helpers import selector
from homeassistant.helpers.schema_config_entry_flow import (
    SchemaConfigFlowHandler,
    SchemaFlowFormStep,
    SchemaFlowMenuStep,
)

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
    DEFAULT_CANCELLATION_PERIOD,
    DEFAULT_RENEWAL_PERIOD,
    DOMAIN,
    RENEWAL_MONTHLY,
    RENEWAL_NONE,
    RENEWAL_YEARLY,
)

OPTIONS_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_COST): selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=0,
                step=0.01,
                mode=selector.NumberSelectorMode.BOX,
            )
        ),
        vol.Optional(CONF_END_DATE): selector.DateSelector(),
        vol.Optional(
            CONF_RENEWAL_PERIOD, default=DEFAULT_RENEWAL_PERIOD
        ): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=[
                    selector.SelectOptionDict(value=RENEWAL_NONE, label="No renewal"),
                    selector.SelectOptionDict(value=RENEWAL_MONTHLY, label="Monthly"),
                    selector.SelectOptionDict(value=RENEWAL_YEARLY, label="Yearly"),
                ],
                mode=selector.SelectSelectorMode.DROPDOWN,
            )
        ),
        vol.Optional(CONF_PROVIDER): selector.TextSelector(),
        vol.Optional(
            CONF_CANCELLATION_PERIOD, default=DEFAULT_CANCELLATION_PERIOD
        ): selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=0,
                max=365,
                mode=selector.NumberSelectorMode.BOX,
            )
        ),
        vol.Optional(CONF_CONTRACT_LENGTH): selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=1,
                max=120,
                mode=selector.NumberSelectorMode.BOX,
            )
        ),
        vol.Optional(CONF_PAYMENT_METHOD): selector.TextSelector(),
        vol.Optional(CONF_ACCOUNT_NUMBER): selector.TextSelector(),
        vol.Optional(CONF_NOTES): selector.TextSelector(
            selector.TextSelectorConfig(
                multiline=True,
            )
        ),
    }
)

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_SUBSCRIPTION_NAME): selector.TextSelector(),
    }
).extend(OPTIONS_SCHEMA.schema)

CONFIG_FLOW: dict[str, SchemaFlowFormStep | SchemaFlowMenuStep] = {
    "user": SchemaFlowFormStep(CONFIG_SCHEMA)
}

OPTIONS_FLOW: dict[str, SchemaFlowFormStep | SchemaFlowMenuStep] = {
    "init": SchemaFlowFormStep(OPTIONS_SCHEMA)
}


class ConfigFlowHandler(SchemaConfigFlowHandler, domain=DOMAIN):
    """Handle a config or options flow for Subscription Helper."""

    config_flow = CONFIG_FLOW
    options_flow = OPTIONS_FLOW

    def async_config_entry_title(self, options: Mapping[str, Any]) -> str:
        """Return config entry title."""
        return cast(str, options[CONF_SUBSCRIPTION_NAME])
