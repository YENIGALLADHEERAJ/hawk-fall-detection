# Sequential benchmarks on the current machine; run only when nothing else is using the CPU/GPU.
$py = '.\.venv\Scripts\python.exe'
& $py -m benchmarks.perception --tag gpu-directml --backend directml --device-id 1 --threads 8
& $py -m benchmarks.perception --tag cpu-32t --backend opencv --threads 32
& $py -m benchmarks.perception --tag cpu-2t --backend opencv --threads 2
# Clean re-run of the CPU 2-thread development set (first run overlapped other work; timings only)
& $py -m evaluation.run --manifest datasets/manifest.json --output evaluation/rtx5060/cpu-2t-dev-rerun --backend opencv --threads 2
