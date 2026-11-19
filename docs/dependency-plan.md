# Dependency plan

## Installed now

Project-local `.venv`: Python 3.12.14 runtime, opencv-python 5.0.0.93 (cv2 5.0.0),
NumPy 2.3.5 and Pydantic 2.14.1 with its resolved transitive dependencies.
All installed application packages are pinned in `requirements-vision.txt`.
No global packages changed. Phase 1 uses standard-library unittest rather than pytest.

On this machine venv ensurepip failed. Installation succeeded using the bundled
runtime's pip with `--python E:\OpenCV\.venv\Scripts\python.exe`. The local venv
currently has no pip module; use that external pip or install pip into the venv
before following the generic README install command.

```powershell
$hawkPython = 'C:\Users\Y SRINIVASA RAO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $hawkPython -m pip --python .\.venv\Scripts\python.exe install -r requirements-vision.txt
.\.venv\Scripts\python.exe scripts/verify_environment.py
```

## Install only when needed

| Phase | Dependencies | Verification gate |
|---|---|---|
| Vision | Audited Zoo ONNX weights; current OpenCV/NumPy | License + hash + real DNN inference + video decode |
| Backend | FastAPI, Pydantic, Uvicorn; pytest/httpx for tests | Resolve exact compatible versions, freeze full environment, schema/API tests |
| AWS | boto3; AWS CLI v2 only for deployment | SSO/role authorization, STS identity, region/model access, no secret output |
| Frontend | React, TypeScript, Vite, Lenis, GSAP | Exact package versions and lockfile, build/typecheck, reduced-motion interaction |
| CI | lint/type tooling, container base | Lock versions and image digest, clean install, CI smoke tests |

Do not invent a complete lockfile before resolving dependencies. Do not install
PyTorch, CUDA, TensorFlow, all four cv2 wheels or AgentCore merely to fill the stack.
The existing Docker client requires a running Linux engine before image builds.
Node 22.20.0 should be checked against the selected Vite release's engine constraint.
The current npm is 8.19.4; a clean lockfile/build is required before accepting that pairing.
