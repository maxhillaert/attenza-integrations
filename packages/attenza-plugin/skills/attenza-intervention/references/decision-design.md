# Design a clear human decision

Use this reference whenever an intervention contains choices or editable fields. Design for a small mobile screen and for a human who may see the intervention without the originating chat.

## Start with the decision shape

| Human decision | Use | Example |
| --- | --- | --- |
| One immediate binary action | Two semantic `Button` actions | `Ship now` / `Hold` |
| Exactly one answer from a list, possibly with other fields | One `ChoicePicker` with `variant: "mutuallyExclusive"`, then one confirmation button | Environment selection plus notes |
| Zero or more related answers | One `ChoicePicker` with `variant: "multipleSelection"` | Files to include |
| One independent yes/no property | One `CheckBox` | Include a backup |
| Free-form correction or explanation | `TextField` | Revised value or reason |

Do not model opposing answers as independent checkboxes. Do not combine a `Hold` or `Reject` option with a second button that means the same thing.

## Actions

- Prefer semantic labels and event names: `Ship now` with `ship_to_staging`, not `Submit` with `submit`.
- Give the surface one visually primary action. A secondary action must represent a genuinely different result.
- For a binary decision, direct action buttons are usually clearer than selecting an option and then submitting it.
- If fields must be reviewed before committing, use one confirmation button and derive the answer from the synchronized `/state`.
- State the consequence of each irreversible or costly action in the surrounding text.

## Content and layout

- Make the title a question or explicit request for a decision.
- Put the decision and its consequence before supporting evidence.
- Include only the facts needed to decide; do not duplicate the title and summary inside the card.
- Use one compact `Card` containing a simple `Column`. Add nested layouts only when they improve scanning.
- Keep option labels short, distinct, and parallel. Avoid labels that require interpreting double negatives.
- Use urgency language only when the deadline is real. The task expiry is authoritative; explain the safe outcome of no response when it matters.
- Never put credentials, private links, or unnecessary personal information in the surface.

## Before sending

Check that:

1. Each possible human outcome has exactly one obvious path.
2. Control cardinality matches the decision cardinality.
3. All editable bindings are initialized under `/state` with the correct type.
4. Machine action names describe outcomes and are not inferred from labels.
5. The intervention remains understandable on its own and fits a mobile viewport without avoidable complexity.
