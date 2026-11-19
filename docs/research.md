# Phase 0 research — 2026-10-25

## Competition findings

The [organizer's submission page](https://opencv26.devpost.com/) requires substantive
OpenCV 5 computation and a meaningful AWS component. Deliver a technical report,
judge-accessible code, pinned setup instructions, architecture diagram, working
endpoint or arranged live demo, evaluation including failures, and a video at most
five minutes showing the team and working system. Agentic eligibility requires
vision results to change a subsequent action; coding-assistant usage alone is insufficient.

The banner closes October 26 at 23:45 PDT, while the overview states 23:59.
Use October 27, **12:15 IST** as the conservative cutoff; aim to upload earlier.
Registration/account eligibility has not been checked. No submission has been made.

The [rules](https://opencv26.devpost.com/rules) weight overall technical execution,
innovation, impact, UX, documentation, and cloud/responsibility at 30/20/20/10/10/10.
Agentic weights are integration 30, autonomy 25, evaluation 20, failure handling and
control 15, presentation 10. COOL weights are verified integration 30, architecture
25, measured value 20, innovation 15, reproducibility 10. Budget engineering time
accordingly. We cannot establish eligibility by implementing only a dashboard.

## OpenCV evidence

[OpenCV's migration notes](https://github.com/opencv/opencv/wiki/OpenCV-5) identify
C++17 as the minimum, removal of the old C API, and relocation of HOG/Haar and
classic ML into contrib. Avoid tutorials that assume those modules remain in core.
[PyPI](https://pypi.org/project/opencv-python/) exposes 5.0.0.93 Windows AMD64 wheels.
We installed that exact distribution; its runtime reports 5.0.0. Only one cv2 wheel
family belongs in an environment. DNN model compatibility still needs a real forward pass.

## Research methodology

| Approach | Why consider it | Limitation / decision |
|---|---|---|
| Detector + bounding-box ratios | Fast baseline, easy temporal features | Camera perspective, sitting and bending confound it; insufficient alone |
| Pose + temporal geometry | Interpretable body transition and recovery cues | Missing joints and occlusion require explicit unknowns; preferred candidate |
| Frame difference | Cheap motion evidence | Lighting/shake create false motion; auxiliary only |
| Optical flow in tracked ROI | Quantifies recovery/movement without retraining | Camera motion and other people contaminate flow; quality-gate it |
| Temporal CNN/LSTM/transformer | Learns temporal discrimination | Dataset, training and deployment validation exceed initial scope |
| Hybrid with active evidence | Can spend compute only on ambiguity | Must show gains over identical perception with fixed verification |

[Video Based Fall Detection Using Human Poses](https://arxiv.org/abs/2107.14633)
motivates temporal pose sequences and 2D-to-3D reasoning; it does not prove our
2D heuristic works. [SSHFD](https://arxiv.org/abs/2004.00797) explores synthetic
training and occluded joints; do not generalize a single-frame result to immobility.
[BoT-SORT](https://arxiv.org/abs/2206.14651) motivates camera-motion compensation
and stronger association, with more machinery than the first controlled-camera demo.
[Revisiting Active Perception](https://arxiv.org/abs/1603.02729) establishes that
active sensing is prior art. Our hypothesis is an application and evaluation contribution.

## Data decision

[UR Fall Detection](https://fenix.ur.edu.pl/~mkepski/ds/uf.html) is a candidate research
dataset with usage conditions; its page asks commercial users to contact the authors.
Do not bundle footage or assume submission publicity rights. Prefer consented staged
clips with safe simulated transitions, never ask someone to perform a dangerous fall.
Store provenance, consent, permitted uses, checksums, camera, subject split and onset
labels in a manifest. Synthetic fixtures validate control flow only. Dataset access,
rights, and a subject-disjoint real-clip evaluation remain open gates.

## Cloud evidence

[Bedrock client-side tools](https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use-client-side.html)
allow a model to request schema-defined tools; our application validates and executes
them and returns results. This fits a small custom orchestration loop.
[AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)
is a hosting/runtime option, not a required reasoning model. Its
[service contract](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-service-contract.html)
supports HTTP/MCP/A2A/AG-UI. Defer it unless managed agent hosting solves an actual
demo problem. Use model IDs and region availability verified in the target account,
not a guessed model string. No live AWS authorization or model invocation was tested.

## UI evidence

[Vite](https://vite.dev/guide/) supports a lightweight local SPA;
[FastAPI](https://fastapi.tiangolo.com/features/) supports typed schemas and WebSockets.
[Lenis](https://github.com/darkroomengineering/lenis) and
[GSAP](https://gsap.com/docs/v3/GSAP/) can animate a replay timeline; retain native
keyboard navigation and disable motion for reduced-motion users. Package pins and
React lifecycle cleanup must be verified at frontend implementation, not assumed here.
