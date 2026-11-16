2026-11-16

- Anonymous GET /recipes → 200 OK, returns all recipes including is_public: false ("Secret family hot sauce").
- Anonymous PATCH /recipes/2 → 200 OK, title changed to "Overnight oats (edited anonymously)".
- Anonymous DELETE /recipes/2 → 204 NO CONTENT, follow-up GET /recipes/2 → 404 NOT FOUND.
