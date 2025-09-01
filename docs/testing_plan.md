# Testing Plan

## Manual
- Input empty ingredients → error shown
- Input "rice, beans" → see at least 1 recipe
- Save a recipe → "Saved!" alert and history appended
- Click "Buy missing items" → opens checkout URL
- Refresh page → app loads

## Automated (placeholder)
- Add unit tests for filter_sample_recipes scoring
- Add route tests for /api/generate and /health

## Performance
- Ensure response under 1s with sample data
- Avoid blocking calls; handle API failures gracefully
