# COOL decision: deferred, not claimed

[OpenCV COOL](https://opencv.org/COOL/) targets optimized visual operations on
AWS Graviton/Arm. Publisher performance claims are not HAWK measurements.
The [competition](https://opencv26.devpost.com/) requires actual core workload
execution on the eligible Arm path. This Windows x86 laptop cannot establish that.

Gate: available AWS account/region, explicit deployment budget, suitable Marketplace
access and confirmed COOL version. Run baseline OpenCV 5 and COOL on the same
Graviton instance type with identical clip hashes, resolution, threads, warmups,
sampling and detector. Log cv2 build information, image ID/digest and package source.
Verify correct numerical outputs and that the claimed kernels actually run in COOL.

Measure repeated end-to-end tool latency p50/p95, frames/second, CPU, memory and
cost per processed minute/incident including Marketplace charges. Separate decode,
DNN and classical kernels. Include installation complexity and failure rates.
Do not compare this laptop against Graviton as evidence of COOL-specific speedup.
Energy efficiency is N/A unless power is measured; CPU percentage is not energy.

Result: N/A. No COOL subscription, instance or benchmark exists. Add
`benchmarks/cool_benchmark.py` when the reproducible core workload exists; a fabricated
microbenchmark now would distract from Tier 1.
