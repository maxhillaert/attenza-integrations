# Author A2UI for Attenza

Use this reference when constructing `a2ui_messages` for `create_intervention`. It is a practical Attenza profile of the official [A2UI v0.9.1 Basic Catalog](https://a2ui.org/specification/v0_9/catalogs/basic/catalog.json), not a replacement schema.

## Message sequence

Send at least these three messages in order, using one stable `surfaceId` throughout:

1. `createSurface` with the official catalog ID and `sendDataModel: true`.
2. `updateComponents` with a non-empty flat component array. The first component is the root; every other component must be reachable by an ID reference.
3. `updateDataModel` whose root value contains `context` and `state` objects.

```json
[
  {
    "version": "v0.9.1",
    "createSurface": {
      "surfaceId": "deploy-choice",
      "catalogId": "https://a2ui.org/specification/v0_9/catalogs/basic/catalog.json",
      "sendDataModel": true
    }
  },
  {
    "version": "v0.9.1",
    "updateComponents": {
      "surfaceId": "deploy-choice",
      "components": []
    }
  },
  {
    "version": "v0.9.1",
    "updateDataModel": {
      "surfaceId": "deploy-choice",
      "value": { "context": {}, "state": {} }
    }
  }
]
```

Do not nest component objects inside other components. `child`, `children`, `content`, and tab `child` values refer to component IDs.

## Data bindings

- Put evidence and non-editable facts below `/context`.
- Put all editable values below `/state` and initialize every bound value.
- Display components may bind to `/context/...` or `/state/...` with `{ "path": "/context/name" }`.
- `TextField`, `CheckBox`, `ChoicePicker`, `Slider`, and `DateTimeInput` values must bind below `/state/`.
- A `CheckBox` value is a boolean. A `ChoicePicker` value is always an array of strings, including for a mutually exclusive picker.
- A mutually exclusive picker must start and finish with zero or one selected value.

## Supported components

Attenza accepts this safe Basic Catalog subset:

| Purpose | Components | Important shape |
| --- | --- | --- |
| Display | `Text`, `Icon`, `Divider` | `Text` requires `text`; use `variant` `h1`-`h5`, `caption`, or `body` only when useful. |
| Layout | `Card`, `Row`, `Column`, `List`, `Tabs`, `Modal` | `Card.child` points to one component; use a `Row` or `Column` to group children. |
| Actions | `Button` | Requires one child component and `action.event.name`; use `variant: "primary"` for the single main action. |
| Input | `TextField`, `CheckBox`, `ChoicePicker`, `Slider`, `DateTimeInput` | Bind `value` below `/state/` and initialize it with the correct JSON type. |

Do not send media components, remote URLs, custom or inline catalogs, themes, styles, classes, functions, or expressions.

## ChoicePicker

Use one `ChoicePicker` for a related set of choices. Its options contain human labels and stable machine values.

```json
{
  "id": "decision",
  "component": "ChoicePicker",
  "label": "Decision",
  "variant": "mutuallyExclusive",
  "displayStyle": "checkbox",
  "options": [
    { "label": "Ship to staging now", "value": "ship" },
    { "label": "Hold — do not ship", "value": "hold" }
  ],
  "value": { "path": "/state/decision" }
}
```

Initialize the binding as `{ "decision": [] }`. Attenza renders a mutually exclusive picker as a single-selection control even though the Basic Catalog calls the ordinary list presentation `checkbox`. Use `variant: "multipleSelection"` only when several options may validly be selected together. `displayStyle: "chips"` changes presentation, not selection cardinality.

Use an individual `CheckBox` only for an independent boolean such as “Include database backup.” Never create separate checkboxes for opposing answers.

## Buttons and actions

A terminal action is a `Button` event. Its name is the durable machine result; the label is presentation only.

```json
{
  "id": "confirm",
  "component": "Button",
  "child": "confirm-label",
  "variant": "primary",
  "action": {
    "event": {
      "name": "confirm_deploy_decision",
      "context": {}
    }
  }
}
```

Every action name must be unique within the surface and remain stable across retries. Read the final synchronized `/state` only after the human invokes an action.

See [`examples/release-approval.json`](../../../../../examples/release-approval.json) for a complete request.
