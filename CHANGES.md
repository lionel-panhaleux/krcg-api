- Upgrade to krcg 5.9. Card and ruling payloads gain a field each, and card
  texts change:
  - Cards named inside another card's text are now marked in place as
    `<Card Name>` and listed in the new `cards` field. Slashes in card text
    are no longer stripped, which fixes 32 mangled texts (`and/or` was served
    as `andor`).
  - Rulings gain a `reminder` boolean, and a group ruling with per-card
    wording now yields each card its own wording.
  - Deck parsing accepts crypt group/advanced qualifiers in parentheses.
