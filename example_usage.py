"""
Example usage of Echocardiographic Myocardial Performance Index (MPI / Tei Index).
Demonstrates normal global cardiac performance vs elevated Tei index in combined heart failure.
"""

from client import MyocardialPerformanceTeiIndexClient

def main():
    client = MyocardialPerformanceTeiIndexClient()

    print("=== Case 1: Healthy Normal LV Performance (Pulsed Doppler) ===")
    normal_case = client.evaluate_tei_index(
        interval_a_ms=385.0,
        ejection_time_et_ms=295.0,
        isovolumetric_relaxation_time_ivrt_ms=50.0,
        modality="Pulsed Wave Doppler",
        ventricle="Left Ventricle"
    )
    print("Cardiac Performance:")
    print(f"  Tei Index (MPI):     {normal_case['tei_metrics']['myocardial_performance_index_mpi']}")
    print(f"  Isovolumetric Total: {normal_case['tei_metrics']['isovolumetric_time_total_ms']} ms")
    print(f"  IVCT / IVRT:         {normal_case['tei_metrics']['ivct_ms']} ms / {normal_case['tei_metrics']['ivrt_ms']} ms")
    print(f"  Status:              {normal_case['cardiac_assessment']['clinical_status']}")

    print("\n=== Case 2: Dilated Cardiomyopathy with Global Impairment ===")
    hf_case = client.evaluate_tei_index(
        interval_a_ms=420.0,
        ejection_time_et_ms=230.0,
        isovolumetric_relaxation_time_ivrt_ms=105.0,
        modality="Pulsed Wave Doppler",
        ventricle="Left Ventricle"
    )
    print("Cardiac Performance:")
    print(f"  Tei Index (MPI):     {hf_case['tei_metrics']['myocardial_performance_index_mpi']} (Markedly elevated!)")
    print(f"  Isovolumetric Total: {hf_case['tei_metrics']['isovolumetric_time_total_ms']} ms")
    print(f"  IVCT / IVRT:         {hf_case['tei_metrics']['ivct_ms']} ms / {hf_case['tei_metrics']['ivrt_ms']} ms")
    print(f"  Status:              {hf_case['cardiac_assessment']['clinical_status']}")
    print(f"  Pathophysiology:     {hf_case['cardiac_assessment']['pathophysiology_summary']}")

if __name__ == "__main__":
    main()
