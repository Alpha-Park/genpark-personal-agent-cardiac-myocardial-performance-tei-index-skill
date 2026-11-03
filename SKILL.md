---
name: genpark-personal-agent-cardiac-myocardial-performance-tei-index-skill
version: 1.0.0
description: Calculates Left and Right Ventricular Tei Index / Myocardial Performance Index (MPI = (a - b) / b).
license: Apache-2.0
compatibility:
  python: ">=3.9"
  openclaw: ">=1.0.0"
  mcp: ">=1.0.0"
---

# Echocardiographic Myocardial Performance Index (MPI / Tei Index) Skill

A zero-dependency personal agent skill for evaluating global ventricular systolic and diastolic mechanical efficiency via Doppler-derived isovolumetric and ejection time intervals.

## Features
- **Geometry-Independent Function**: Assesses global myocardial pump performance without geometric chamber shape assumptions.
- **Isovolumetric Phase Partitioning**: Computes total isovolumetric time ($IVCT + IVRT = a - b$), separating contraction and relaxation delays.
- **Tei Index ($MPI$)**: Measures $(a - b) / b$, benchmarking against pulsed Doppler ($< 0.40$) and Tissue Doppler ($< 0.45$) guidelines.
- **Chamber Specificity**: Supports both Left Ventricular and Right Ventricular evaluations.

## MCP Server Integration
Exposes `evaluate_tei_index` for autonomous cardiac risk stratification, cardiotoxicity surveillance, and heart failure monitoring.
