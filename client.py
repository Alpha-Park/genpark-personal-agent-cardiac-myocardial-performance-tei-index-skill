"""
Echocardiographic Myocardial Performance Index (MPI / Tei Index) Client.
Zero-mock pure Python standard library implementation.
Calculates Left and Right Ventricular Tei Index (MPI = (IVCT + IVRT) / ET = (a - b) / b),
isovolumetric phase partitioning, and global systolic-diastolic cardiac function staging.
"""

import math
from typing import Dict, Any, Optional


class MyocardialPerformanceTeiIndexClient:
    """
    Evaluates global left and right ventricular performance independent of geometric assumptions:
    - a (ms): interval from cessation to onset of atrioventricular inflow (IVCT + ET + IVRT)
    - b / ET (ms): ventricular ejection time
    - IVCT (ms): isovolumetric contraction time
    - IVRT (ms): isovolumetric relaxation time
    - MPI (Tei Index) = (IVCT + IVRT) / ET = (a - b) / b
    - Evaluates subclinical myocardial strain, heart failure, and cardiotoxicity.
    """

    def __init__(self):
        pass

    def evaluate_tei_index(
        self,
        interval_a_ms: float,
        ejection_time_et_ms: float,
        isovolumetric_relaxation_time_ivrt_ms: Optional[float] = None,
        modality: Optional[str] = "Pulsed Wave Doppler",
        ventricle: Optional[str] = "Left Ventricle",
        heart_rate_bpm: Optional[float] = 72.0
    ) -> Dict[str, Any]:
        """
        Calculates Myocardial Performance Index (Tei Index).
        interval_a_ms: interval from inflow cessation to inflow onset in ms (e.g. 390.0 ms).
        ejection_time_et_ms: ventricular ejection time ET (b) in ms (e.g. 290.0 ms).
        isovolumetric_relaxation_time_ivrt_ms: measured IVRT in ms (optional, e.g. 60.0 ms).
        modality: 'Pulsed Wave Doppler' or 'Tissue Doppler Imaging (TDI)'.
        ventricle: 'Left Ventricle' or 'Right Ventricle'.
        """
        if interval_a_ms <= 0 or ejection_time_et_ms <= 0:
            raise ValueError("Doppler time intervals must be strictly positive.")
        if interval_a_ms <= ejection_time_et_ms:
            raise ValueError("Inflow cessation interval 'a' must exceed ejection time 'ET'.")

        # Total isovolumetric time (IVCT + IVRT in ms)
        isovolumetric_time_ms = interval_a_ms - ejection_time_et_ms

        # Tei Index (MPI)
        mpi = isovolumetric_time_ms / ejection_time_et_ms

        # Calculate IVCT if IVRT is provided
        ivct_ms = None
        if isovolumetric_relaxation_time_ivrt_ms is not None:
            if isovolumetric_relaxation_time_ivrt_ms >= isovolumetric_time_ms:
                raise ValueError("IVRT cannot exceed total isovolumetric time (a - b).")
            ivct_ms = round(isovolumetric_time_ms - isovolumetric_relaxation_time_ivrt_ms, 1)

        # Reference thresholds based on ASE/EACVI consensus:
        # Left Ventricle:
        #   PW Doppler: Normal < 0.40, Borderline 0.40 - 0.47, Elevated > 0.47
        #   Tissue Doppler: Normal < 0.45, Borderline 0.45 - 0.54, Elevated > 0.54
        # Right Ventricle:
        #   PW Doppler: Normal < 0.28, Elevated >= 0.28
        #   Tissue Doppler: Normal < 0.55, Elevated >= 0.55
        is_tdi = "tissue" in modality.lower()
        is_rv = "right" in ventricle.lower()

        if is_rv:
            threshold_normal = 0.55 if is_tdi else 0.28
            if mpi > threshold_normal:
                clinical_status = "Elevated Right Ventricular MPI (RV Dysfunction / Cor Pulmonale)"
                pathophysiology = "Prolonged RV isovolumetric phases relative to ejection; indicates pulmonary arterial hypertension or RV cardiomyopathy."
            else:
                clinical_status = "Normal Right Ventricular Myocardial Performance"
                pathophysiology = "Preserved RV global systolic and diastolic ventricular kinetics."
        else:
            threshold_normal = 0.45 if is_tdi else 0.40
            threshold_moderate = 0.54 if is_tdi else 0.48
            if mpi > threshold_moderate:
                clinical_status = "Moderately-to-Severely Impaired Global LV Performance"
                pathophysiology = "Dual impairment of systolic contractility (prolonged IVCT) and active myocardial lusitropy (delayed IVRT); high risk of heart failure decompensation."
            elif mpi > threshold_normal:
                clinical_status = "Mildly Elevated Tei Index / Subclinical Dysfunction"
                pathophysiology = "Subtle uncoupling of isovolumetric contraction and relaxation phases; early hypertensive heart disease or subclinical ischemic strain."
            else:
                clinical_status = "Preserved Global Ventricular Performance / Normal Tei Index"
                pathophysiology = "Equilibrated isovolumetric and ejection phases; robust cardiac energetic efficiency."

        return {
            "status": "success",
            "tei_metrics": {
                "myocardial_performance_index_mpi": round(mpi, 3),
                "isovolumetric_time_total_ms": round(isovolumetric_time_ms, 1),
                "ejection_time_et_ms": round(ejection_time_et_ms, 1),
                "inflow_interval_a_ms": round(interval_a_ms, 1),
                "ivct_ms": ivct_ms,
                "ivrt_ms": isovolumetric_relaxation_time_ivrt_ms
            },
            "examination_context": {
                "ventricle": ventricle,
                "modality": modality,
                "heart_rate_bpm": heart_rate_bpm
            },
            "cardiac_assessment": {
                "clinical_status": clinical_status,
                "pathophysiology_summary": pathophysiology
            }
        }
