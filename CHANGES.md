- Upgrade to krcg 5.12. Ruling payloads gain a field, and card data changes:
  - Ruling `symbols` gain a `count`: a cost marker like `[1 CONVICTION]` now
    parses (37 occurrences over 29 card texts), and the digit is served apart
    from the glyph, as `{"text": "[1 CONVICTION]", "symbol": "¤", "count": "1"}`.
  - Ruling texts may name a card by id, `{101565|Rebirth}`, so a card token
    survives a rename. The bare `{Rebirth}` form still occurs.
  - Anthology keeps its `LARP` bundle: the 11 cards Anthology I did not reprint
    no longer get a spurious `Ant1` print.
  - Path of Death and the Soul on Burial Site Hunting Ground and Sakura, The
    Merciless is no longer marked as a card: it names the Sabbat path.
  - Promo Pack 1 bundle size is 56, not 59.
- Deck import: a dead Amaranth deck id answers 400 instead of a 500. A dead
  VDB deck id still answers 502, now carrying VDB's own error rather than a
  content-type complaint. VDB "deck in URL" links (`/decks/deck#...`) import
  correctly.
