# Subscription Helper

[![GitHub Release](https://img.shields.io/github/release/mariobrosch/subscription-helper.svg?style=flat-square)](https://github.com/mariobrosch/subscription-helper/releases)
[![License](https://img.shields.io/github/license/mariobrosch/subscription-helper.svg?style=flat-square)](LICENSE)

Track and manage all your subscriptions in Home Assistant!

## Features

- ✅ **Multiple subscriptions**: Add unlimited subscriptions
- 📅 **End date tracking**: Keep track of when subscriptions expire
- 💰 **Cost tracking**: Store costs per period per subscription
- 🔄 **Auto-renewal support**: Support for monthly/yearly renewal
- 🔔 **Status sensor**: "Active", "Expiring soon" (7 days), "Expired"
- 📊 **Days remaining sensor**: Exact countdown to end date
- 📝 **Extra fields**: Provider, cancellation period, payment method, account number, notes
- 🌍 **Multi-language**: Fully translated to Dutch and English

## Quick Start

After installation via HACS:

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for **Subscription Helper**
4. Fill in your subscription details

## Automation Examples

### Notification for expiring subscription

```yaml
automation:
  - alias: "Notify expiring subscription"
    trigger:
      - platform: state
        entity_id: sensor.netflix_status
        to: "expiring_soon"
    action:
      - service: notify.mobile_app
        data:
          title: "Subscription expiring soon"
          message: "Your Netflix subscription expires in {{ state_attr('sensor.netflix_status', 'days_remaining') }} days"
```

### Auto-update end date for monthly subscription

```yaml
automation:
  - alias: "Update Netflix subscription"
    trigger:
      - platform: state
        entity_id: sensor.netflix_status
        to: "expired"
    action:
      - service: subscription_helper.update_options
        data:
          entity_id: sensor.netflix_status
          end_date: "{{ (now() + timedelta(days=30)).strftime('%Y-%m-%d') }}"
```

For more examples and detailed documentation, see the [README](https://github.com/mariobrosch/subscription-helper).
