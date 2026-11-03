# Echocardiographic Myocardial Performance Index (MPI / Tei Index) Skill

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Model Context Protocol](https://img.shields.io/badge/MCP-Standard-green.svg)](https://modelcontextprotocol.io/)
[![Zero External Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)](requirements.txt)
[![Status: Production-Ready](https://img.shields.io/badge/status-production--ready-success.svg)](https://github.com/alphaparkinc)

A zero-dependency, mathematically rigorous personal agent skill that computes the Doppler Tei Index (Myocardial Performance Index) to evaluate combined ventricular systolic and diastolic function.

## Architecture

```mermaid
flowchart TD
    A[Mitral and Aortic Doppler Signals] --> B[Measure Inflow Interval a & Ejection Time b]
    B --> C[Compute Isovolumetric Time = a - b]
    C --> D[Compute Tei Index MPI = (a - b) / b]
    D --> E[Benchmark vs ASE/EACVI PW and TDI Thresholds]
    E --> F[Global Cardiac Performance & Lusitropic Guidance]
```

## Quick Start

```python
from client import MyocardialPerformanceTeiIndexClient

client = MyocardialPerformanceTeiIndexClient()
result = client.evaluate_tei_index(
    interval_a_ms=385.0,
    ejection_time_et_ms=295.0,
    isovolumetric_relaxation_time_ivrt_ms=50.0
)
print("Tei Index (MPI):", result["tei_metrics"]["myocardial_performance_index_mpi"])
print("Status:", result["cardiac_assessment"]["clinical_status"])
```

## License
Apache-2.0
