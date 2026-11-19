# Environment audit — 2026-10-25

| Item | Observed result |
|---|---|
| Workspace | E:\OpenCV initially empty; no Git repository or AGENTS.md |
| OS | Windows 11, build 26300, AMD64 |
| CPU | Intel Core i5-10210U @ 1.60 GHz |
| RAM | 7.79 GiB usable physical memory via GlobalMemoryStatusEx |
| GPU | NVIDIA GeForce MX250, 2048 MiB, nvidia-smi works |
| Python on PATH | C:\Windows\system32\python fails with access denied |
| Working Python | Bundled CPython 3.12.14; path in dependency plan |
| Node / npm | 22.20.0 / 8.19.4 |
| pnpm / bun | pnpm launcher present, version not verified; bun absent |
| Docker | Client 29.8.0; Linux daemon pipe absent/unavailable |
| Git | 2.50.1.windows.1 |
| AWS | CLI absent; standard config/credentials files absent; no AWS-prefixed environment names found |
| CUDA | nvcc absent; GPU driver presence does not establish CUDA toolchain |
| Compiler | cl and cmake absent from PATH; Visual Studio installation not exhaustively searched |
| OpenCV | Initially absent; isolated 5.0.0.93 wheel installed and runtime 5.0.0 verified |

CIM hardware queries were denied. RAM was obtained with a Windows memory API and CPU
name from registry output. Do not interpret the initial failed CIM report's zero RAM
as a measurement. No AWS secret values were read or printed. Lack of local config
does not prove the user lacks an AWS account.

Initial venv ensurepip failed; external pip installed only the two pinned vision
packages. Sandbox DNS failed on PyPI; the authorized network retry succeeded.
See [machine-readable measurements](environment-verification.json).

The probe checks OpenCV major version, color conversion, resize, frame difference,
PNG round trip and Farneback flow against a known three-pixel shift. It checks DNN
and capture API presence only; neither model inference nor real video decoding is
yet validated. No end-to-end FPS, fall accuracy, cloud cost or COOL results exist.

## Re-audit on new machine — 2026-11-15

The project moved to a different machine; the table above describes the previous one.

| Item | Observed result |
|---|---|
| Workspace | D:\OpenCV (git repo, no commits yet) |
| CPU | AMD Ryzen 9 9955HX, 16 cores / 32 threads |
| RAM | 15.2 GiB |
| GPU | NVIDIA GeForce RTX 5060 Laptop, 8 GiB, driver 621.14, CUDA UMD 13.5; plus AMD integrated graphics |
| Free disk (D:) | about 199 GB |
| Python | 3.11.1 (`C:\Program Files\Python311`); the `python` on PATH is a Store stub. The old 3.12 venv pointed at a missing path and was renamed `.venv-broken-old` |
| Venv | New `.venv` on Python 3.11 with the unchanged pins in `requirements-vision.txt` (OpenCV 5.0.0.93 is an abi3 wheel) |
| `verify_environment.py` | passed (OpenCV 5.0.0, DNN and capture available) |
| Test suite | 54/54 passed in 27.1 s (100 s on the old machine) |

Install workaround: pip stalled fetching the `pydantic-core` index page (default connection). `curl -4 --http1.1` fetched it; the `pydantic_core-2.50.1-cp311-cp311-win_amd64.whl` was downloaded directly, its SHA-256 matched the index (`0048b6dd...dd1bc`), then it was installed with `--no-deps` and the pinned requirements installed normally.

Open item: OpenCV 5 logs "Targets are not supported by the new graph engine for now" when `setPreferableTarget` is called, and the pip wheel has no CUDA, so the RTX 5060 is unused. Detector timings have not been re-measured here; the 1.46 FPS figure is from the old machine.

Update the same day: added optional `onnxruntime-directml` 1.24.4 for the GPU detector backend; RTX 5060 is DirectML adapter 1 (6.1 ms vs 142.9 ms per inference at the old 2-thread CPU setting). See [hardware-rtx5060.md](hardware-rtx5060.md) for all measurements; the open item above is resolved by the ONNX Runtime backend.
