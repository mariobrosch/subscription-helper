# Subscription Helper for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

A helpful Home Assistant integration to manage and track all your subscriptions and when they expire. This can help you get implement notifications via automations so you get notified when a subscription is getting to an end and you need to take action or not.

For many contracts or subscription auto renewal is done, so this can also being set as a property so you can create an automation to update the end date when a subscription is ended. See example below.

## Features

- ✅ **Multiple subscriptions**: Add unlimited subscriptions
- 📅 **End date tracking**: Keep track of when subscriptions expire
- 💰 **Cost tracking**: Store costs per period per subscription
- 🔄 **Auto-renewal support**: Support for monthly/yearly renewal
- 🔔 **Status sensor**: "Active", "Expiring soon" (7 days), "Expired"
- 📊 **Days remaining sensor**: Exact countdown to end date
- 📝 **Extra fields**: Provider, cancellation period, payment method, account number, notes
- 🌍 **Multi-language**: Fully translated to Dutch and English

## Installation

### Via HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots in the top right
4. Select "Custom repositories"
5. Add this repository: `https://github.com/mariobrosch/subscription-helper`
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
2. Click **+ Add Integration** (or go to **Helper**-tab and click **Add Helper**)
3. Search for **Subscription Helper**
4. Fill in the details:
   - **Subscription name**: Name of your subscription (e.g., Netflix, Spotify)
   - **Monthly cost** (optional): Cost per period
   - **End date** (optional): When does this subscription expire?
   - **Renewal period**: None, Monthly, or Yearly
   - **Provider** (optional): Company providing the service
   - **Cancellation period** (optional): Days notice needed to cancel
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
- `payment_method`
- `account_number`
- `notes`

## Services

### `subscription_helper.update_options`

Updates the configuration of an existing subscription. Useful for automations that automatically extend renewal dates or update other fields.

**Parameters:**

You can identify the subscription using **either** parameter:

- `entity_id` (recommended): The entity ID of any sensor belonging to the subscription (e.g., `sensor.netflix_status`)
- `config_entry_id`: The config entry ID (advanced usage)

**Updatable fields** (all optional - only include what you want to change):

- `subscription_name`: Change the subscription name
- `cost`: Update cost per period
- `end_date`: Set a new end date (format: `YYYY-MM-DD`)
- `renewal_period`: Change renewal period (`none`, `monthly`, or `yearly`)
- `provider`: Update provider name
- `cancellation_period`: Change cancellation period in days
- `payment_method`: Update payment method
- `account_number`: Change account/contract number
- `notes`: Update notes

**Example usage:**

```yaml
# Simple: Update only the end date
action: subscription_helper.update_options
data:
  entity_id: sensor.netflix_status
  end_date: "2026-12-31"

# Advanced: Update multiple fields at once
action: subscription_helper.update_options
data:
  entity_id: sensor.spotify_status
  cost: 12.99
  end_date: "2027-01-15"
  payment_method: "Credit Card"
```

**Developer Tools testing:**

You can test the service in **Developer Tools > Actions**:

1. Search for `subscription_helper.update_options`
2. Fill in the entity_id and field(s) you want to update
3. Click "Perform action"

## Subscription types

I intentionally did not create any subscription types (streaming, insurence, contracts, etc.), because they will change over time and are never suitable for anyones needs. Use the labels of Home Assistant too add categories or group the same types.

### Example of using labels

When adding your subscription for streaming services create a new label in home assistant. For example with the name `subscription_streaming`. When creating multiple new helpers for example Netflix, Disney+, Amazone Prima, HBO, etc. Just add the created label to that helper and create groups like this. This way you can create automations or other insights on how you want to use it.

### Automation Examples

**Auto-renew subscription after expiration:**

This automation automatically extends the end date when a subscription expires and has a renewal period set. If you don't want automatic renewal, set the renewal period to "None" when configuring the subscription.

```yaml
automation:
  - alias: "Auto-renew expired subscriptions"
    triggers:
      - entity_id:
          - sensor.netflix_status
          - sensor.spotify_status
          # Add more subscription status sensors here
        to: expired
        trigger: state
    conditions:
      - condition: template
        value_template: >
          {{ state_attr(trigger.to_state.entity_id, 'renewal_period') != 'none' }}
    actions:
      - action: subscription_helper.update_options
        data:
          entity_id: "{{ trigger.to_state.entity_id }}"
          end_date: >
            {% set entity = trigger.to_state.entity_id %}
            {% set current_end = state_attr(entity, 'end_date') %}
            {% set renewal = state_attr(entity, 'renewal_period') %}
            {% if renewal == 'monthly' %}
              {{ (strptime(current_end, '%Y-%m-%d') + timedelta(days=30)).strftime('%Y-%m-%d') }}
            {% elif renewal == 'yearly' %}
              {{ (strptime(current_end, '%Y-%m-%d') + timedelta(days=365)).strftime('%Y-%m-%d') }}
            {% endif %}
      - action: notify.mobile_app
        data:
          message: >
            {{ trigger.to_state.attributes.friendly_name }} has been automatically renewed.
            New end date: {{ state_attr(trigger.to_state.entity_id, 'end_date') }}
```

**Important testing notes:**

- ⚠️ Do NOT use "Run all actions" to test - it doesn't provide trigger context
- ✅ Test by changing sensor state: Developer Tools > States > set to `active`, then to `expired`
- ✅ Make sure the subscription has a renewal period (not "None") or the condition will block the automation

**Auto-renew subscriptions based on label (time-based):**

Instead of listing all entities individually, you can use a label to group subscriptions. This makes it easier to manage multiple subscriptions.

First, create a label in Home Assistant (e.g., "subscription_auto_renew") and add it to the subscription helper config entries you want to auto-renew.

```yaml
automation:
  - alias: "Auto-renew labeled subscriptions"
    triggers:
      - at: "00:00:00"
        trigger: time
    actions:
      - repeat:
          for_each: >
            {{ expand(label_entities('subscription_auto_renew'))
               | selectattr('entity_id', 'match', '.*_status$')
               | selectattr('state', 'eq', 'expired')
               | selectattr('attributes.renewal_period', 'defined')
               | selectattr('attributes.renewal_period', 'ne', 'none')
               | map(attribute='entity_id')
               | list }}
          sequence:
            - action: subscription_helper.update_options
              data:
                entity_id: "{{ repeat.item }}"
                end_date: >
                  {% set current_end = state_attr(repeat.item, 'end_date') %}
                  {% set renewal = state_attr(repeat.item, 'renewal_period') %}
                  {% if renewal == 'monthly' %}
                    {{ (strptime(current_end, '%Y-%m-%d') + timedelta(days=30)).strftime('%Y-%m-%d') }}
                  {% elif renewal == 'yearly' %}
                    {{ (strptime(current_end, '%Y-%m-%d') + timedelta(days=365)).strftime('%Y-%m-%d') }}
                  {% endif %}
            - action: notify.mobile_app
              data:
                message: >
                  {{ state_attr(repeat.item, 'friendly_name') }} has been automatically renewed.
                  New end date: {{ state_attr(repeat.item, 'end_date') }}
```

### Automation Examples

**Auto-renew subscription after expiration:**

This automation automatically extends the end date when a subscription expires and has a renewal period set. If you don't want automatic renewal, set the renewal period to "None" when configuring the subscription.

```yaml
automation:
  - alias: "Auto-renew expired subscriptions"
    trigger:
      - platform: state
        entity_id:
          - sensor.netflix_status
          - sensor.spotify_status
          # Add more subscription status sensors here
        to: "expired"
    condition:
      - condition: template
        value_template: >
          {{ state_attr(trigger.entity_id, 'renewal_period') != 'none' }}
    action:
      - service: subscription_helper.update_options
        data:
          entity_id: "{{ trigger.entity_id }}"
          end_date: >
            {% set current_end = state_attr(trigger.entity_id, 'end_date') %}
            {% set renewal = state_attr(trigger.entity_id, 'renewal_period') %}
            {% if renewal == 'monthly' %}
              {{ (strptime(current_end, '%Y-%m-%d') + timedelta(days=30)).strftime('%Y-%m-%d') }}
            {% elif renewal == 'yearly' %}
              {{ (strptime(current_end, '%Y-%m-%d') + timedelta(days=365)).strftime('%Y-%m-%d') }}
            {% endif %}
      - service: notify.mobile_app
        data:
          message: >
            {{ trigger.to_state.name }} has been automatically renewed.
            New end date: {{ state_attr(trigger.entity_id, 'end_date') }}
```

**Auto-renew subscriptions based on label (recommended):**

Instead of listing all entities individually, you can use a label to group subscriptions. This makes it easier to manage multiple subscriptions.

First, create a label in Home Assistant (e.g., "subscription_auto_renew") and add it to the subscription helper config entries you want to auto-renew.

```yaml
automation:
  - alias: "Auto-renew labeled subscriptions"
    trigger:
      - platform: state
        entity_id: sensor.time # Or use a time pattern trigger
    condition:
      - condition: template
        value_template: >
          {{ expand(label_entities('subscription_auto_renew'))
             | selectattr('attributes.status', 'eq', 'expired')
             | selectattr('attributes.renewal_period', 'ne', 'none')
             | list | count > 0 }}
    action:
      - repeat:
          for_each: >
            {{ expand(label_entities('subscription_auto_renew'))
               | selectattr('attributes.status', 'eq', 'expired')
               | selectattr('attributes.renewal_period', 'ne', 'none')
               | map(attribute='entity_id')
               | list }}
        sequence:
          - service: subscription_helper.update_options
            data:
              entity_id: "{{ repeat.item }}"
              end_date: >
                {% set current_end = state_attr(repeat.item, 'end_date') %}
                {% set renewal = state_attr(repeat.item, 'renewal_period') %}
                {% if renewal == 'monthly' %}
                  {{ (strptime(current_end, '%Y-%m-%d') + timedelta(days=30)).strftime('%Y-%m-%d') }}
                {% elif renewal == 'yearly' %}
                  {{ (strptime(current_end, '%Y-%m-%d') + timedelta(days=365)).strftime('%Y-%m-%d') }}
                {% endif %}
          - service: notify.mobile_app
            data:
              message: >
                {{ state_attr(repeat.item, 'friendly_name') }} has been automatically renewed.
```

This automation works for all subscriptions with a specific label. First, add a label (e.g., `subscription_auto_renew`) to the subscriptions you want to auto-renew.

```yaml
automation:
  - alias: "Auto-renew labeled subscriptions"
    trigger:
      - platform: state
        to: "expired"
    condition:
      - condition: template
        value_template: >
          {{ trigger.entity_id.endswith('_status')
             and 'subscription_auto_renew' in state_attr(trigger.entity_id, 'labels') | default([])
             and state_attr(trigger.entity_id, 'renewal_period') != 'none' }}
    action:
      - service: subscription_helper.update_options
        target:
          entity_id: "{{ trigger.entity_id }}"
        data:
          end_date: >
            {% set current_end = state_attr(trigger.entity_id, 'end_date') %}
            {% set renewal = state_attr(trigger.entity_id, 'renewal_period') %}
            {% if renewal == 'monthly' %}
              {{ (strptime(current_end, '%Y-%m-%d') + timedelta(days=30)).strftime('%Y-%m-%d') }}
            {% elif renewal == 'yearly' %}
              {{ (strptime(current_end, '%Y-%m-%d') + timedelta(days=365)).strftime('%Y-%m-%d') }}
            {% endif %}
      - service: notify.mobile_app
        data:
          message: >
            {{ trigger.to_state.name }} has been automatically renewed.
            New end date: {{ state_attr(trigger.entity_id, 'end_date') }}
```

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
