"""Constants for the Subscription Helper integration."""

DOMAIN = "subscription_helper"

# Configuration fields
CONF_SUBSCRIPTION_NAME = "subscription_name"
CONF_COST = "cost"
CONF_END_DATE = "end_date"
CONF_RENEWAL_PERIOD = "renewal_period"
CONF_PROVIDER = "provider"
CONF_CANCELLATION_PERIOD = "cancellation_period"
CONF_PAYMENT_METHOD = "payment_method"
CONF_ACCOUNT_NUMBER = "account_number"
CONF_NOTES = "notes"

# Default values
DEFAULT_RENEWAL_PERIOD = "none"
DEFAULT_CANCELLATION_PERIOD = 30

# Expiring soon threshold (days)
EXPIRING_SOON_DAYS = 7

# Renewal period options
RENEWAL_NONE = "none"
RENEWAL_MONTHLY = "monthly"
RENEWAL_YEARLY = "yearly"
