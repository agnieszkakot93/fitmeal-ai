"""Shopping list (PRD §8.10): pure functions, no database or I/O.

:func:`app.shopping.aggregate.needs_from_plan` turns a planner plan into
per-food gram needs, :func:`app.shopping.aggregate.build_list` groups and
annotates them, and :func:`app.shopping.merge.merge` carries checkbox state
over to a regenerated list. No pricing yet (Phase 2).
"""
