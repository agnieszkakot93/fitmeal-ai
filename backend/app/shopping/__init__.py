"""Shopping list aggregation (PRD §8.10): pure functions, no database or I/O.

Entry point: :func:`app.shopping.aggregate.build_list`. Checkbox state is not
part of the list; it is stored separately, keyed by food, so it survives
regeneration.
"""
