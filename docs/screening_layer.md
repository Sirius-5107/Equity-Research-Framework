# Screening Layer

The screening layer converts scored factor data into an eligible, ranked
candidate set.

1. Eligibility: required fields and explicit constraints.
2. Ranking: deterministic cross-sectional ranking by a chosen score.
3. Selection: top-N candidates.

Filters remain separate from factor definitions, allowing experiments to change
eligibility without rewriting factor calculations. No default financial
threshold is treated as universally correct; constraints should be justified
by the research question and recorded in experiment configuration.
