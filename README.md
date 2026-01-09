# Subscription Helper for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

A helpful Home Assistant integration to manage and track all your subscriptions and when they expire.

## Features

- ✅ **Multiple subscriptions**: Add unlimited subscriptions
- 📅 **End date tracking**: Keep track of when subscriptions expire
- 💰 **Cost tracking**: Store monthly costs per subscription
- 🔄 **Auto-renewal support**: Support for monthly/yearly renewal
- 🔔 **Status sensor**: "Active", "Expiring soon" (7 days), "Expired"
- 📊 **Days remaining sensor**: Exact countdown to end date
- 📝 **Extra fields**: Provider, cancellation period, contract length, payment method, account number, notes
- 🌍 **Multi-language**: Fully translated to Dutch and English

## Installation

### Via HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots in the top right
4. Select "Custom repositories"
5. Add this repository: `https://github.com/YOUR_USERNAME/subscription-helper`
6. Select category "Integration"
7. Click "Add"
8. Search for "Subscription Helper"
9. Click "Download"
10. Restart Home Assistant

### Manual Installation

1. Download the `custom_components/subscription_helper` folder
2. Copy it to `<config>/custom_components/subscription_helper`
3. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for **Subscription Helper**
4. Fill in the details:
   - **Subscription name**: Name of your subscription (e.g., Netflix, Spotify)
   - **Monthly cost** (optional): Cost per month
   - **End date** (optional): When does this subscription expire?
   - **Renewal period**: None, Monthly, or Yearly
   - **Provider** (optional): Company providing the service
   - **Cancellation period** (optional): Days notice needed to cancel
   - **Contract length** (optional): Duration in months (12, 24, etc.)
   - **Payment method** (optional): How you pay
   - **Account number** (optional): Contract or account number
   - **Notes** (optional): Additional information

## Usage

### Sensors

Two sensors are created for each subscription:

1. **`sensor.NAME_days_remaining`**: Days until end date
2. **`sensor.NAME_status`**: Status (active/expiring_soon/expired)

### Attributes

The status sensor contains all extra information as attributes:
- `end_date`
- `cost`
- `renewal_period`
- `provider`
- `cancellation_period`
- `contract_length`
- `payment_method`
- `account_number`
- `notes`

### Automation Examples

**Notification 7 days before expiration:**
```yaml
automation:
  - alias: "Subscription expiring soon"
    trigger:
      - platform: state
        entity_id: sensor.netflix_status
        to: "expiring_soon"
    action:
      - service: notify.mobile_app
        data:
          message: "Your Netflix subscription expires in {{ state_attr('sensor.netflix_days_remaining', 'state') }} days!"
```

**Dashboard card:**
```yaml
type: entities
title: My Subscriptions
entities:
  - entity: sensor.netflix_status
    secondary_info: last-changed
  - entity: sensor.netflix_days_remaining
  - entity: sensor.spotify_status
  - entity: sensor.spotify_days_remaining
```

**Overview dashboard with template:**
```yaml
type: markdown
content: |
  ## Expiring Soon
  {% for state in states.sensor 
     if state.entity_id.endswith('_status') 
     and state.state == 'expiring_soon' %}
  - **{{ state.name }}**: {{ state.attributes.days_remaining }} days
  {% endfor %}
```

## Support

For questions, bugs, or feature requests, please open an issue on GitHub.

## License

MIT License - see LICENSE file for details.
