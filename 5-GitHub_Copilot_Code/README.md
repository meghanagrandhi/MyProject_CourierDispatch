# 5 - GitHub Copilot Generated Code

Code for the Hyperlocal Courier Dispatch & Tracking Engine, generated with GitHub Copilot from a single prompt and then reviewed and corrected.

| File | Requirement |
|---|---|
| models.py | Data models (Rider, CourierRequest, status values) |
| request_service.py | FR-002: create courier request |
| matching.py | FR-001: nearest active rider within 3 km |
| dispatch.py | FR-003: accept / reject and reassignment |
| routing.py | FR-004: route planning and optimization |
| delivery.py | FR-005: OTP generation and verification |
| tracking.py | NFR-001: status and GPS updates, latency measurement |
| main.py | Demo of the full flow |
| test_courier.py | pytest tests for the acceptance criteria |

## How to run
```
pip install -r requirements.txt
python main.py
pytest -v
```

## Screenshots
Copilot prompt and generated code, test results and demo output are in the screenshots included in this folder.
