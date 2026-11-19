# Positioning and defensible contribution

Fall detection, pose heuristics, temporal verification, tracking, safety dashboards
and active perception all have prior art. Ambianic already combines pose and temporal
heuristics; SentinelCV already connects CCTV fall candidates to alerts. See the
[source and license ledger](open-source-landscape.md).

HAWK's proposed contribution is a reproducible, budgeted evidence-acquisition policy
that chooses which visual computation to perform next, retains an inspectable trace,
and tests whether that policy improves decisions at acceptable latency and cost.
This is an unproven contribution until evaluated, not a claim of global novelty.

Reuse: OpenCV numerical/image operations and audited pretrained models.
Common engineering: typed API, event queue, dashboard, human review.
Original project work: evidence sufficiency contract, bounded selection policy,
failure handling, paired evaluation and operator-facing provenance.

The decisive comparator is not only immediate alerting: a fixed temporal-verification
pipeline may achieve the same benefit. Include it as a second baseline. If active
selection does not beat it, report that result and explain whether compute savings
or traceability still provide value. An LLM is not automatically the better planner.
