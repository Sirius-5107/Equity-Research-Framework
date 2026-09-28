# Fundamentals Layer

This layer contains reusable statement parsing and financial metrics migrated from
the Summer-Project.

## Design

- Statement-row aliases are centralized in get_metric.
- latest_value explicitly handles Yahoo Finance's newest-first statement layout.
- Ratios return NaN for missing inputs or zero denominators.
- CAGR expects observations ordered oldest-to-newest and uses an explicit periods_per_year argument.
- Fundamental metrics live in the data layer; factor weighting and ranking belong in factors/ and screening/.

The old hard-coded fundamental filters and quality/growth weights are not migrated.
Those are research choices and should become configurable factors after the raw metric layer is validated.
