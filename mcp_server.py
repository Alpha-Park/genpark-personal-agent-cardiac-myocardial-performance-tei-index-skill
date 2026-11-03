"""
MCP Server for Echocardiographic Myocardial Performance Index (MPI / Tei Index).
Exposes tools for combined systolic and diastolic cardiac function assessment.
"""

import json
from typing import Dict, Any, Optional
from client import MyocardialPerformanceTeiIndexClient


def handle_evaluate_tei(params: Dict[str, Any]) -> Dict[str, Any]:
    interval_a_ms = float(params.get("interval_a_ms", 390.0))
    ejection_time_et_ms = float(params.get("ejection_time_et_ms", 290.0))
    isovolumetric_relaxation_time_ivrt_ms = params.get("isovolumetric_relaxation_time_ivrt_ms")
    if isovolumetric_relaxation_time_ivrt_ms is not None:
        isovolumetric_relaxation_time_ivrt_ms = float(isovolumetric_relaxation_time_ivrt_ms)
    modality = str(params.get("modality", "Pulsed Wave Doppler"))
    ventricle = str(params.get("ventricle", "Left Ventricle"))
    heart_rate_bpm = float(params.get("heart_rate_bpm", 72.0))

    client = MyocardialPerformanceTeiIndexClient()
    return client.evaluate_tei_index(
        interval_a_ms=interval_a_ms,
        ejection_time_et_ms=ejection_time_et_ms,
        isovolumetric_relaxation_time_ivrt_ms=isovolumetric_relaxation_time_ivrt_ms,
        modality=modality,
        ventricle=ventricle,
        heart_rate_bpm=heart_rate_bpm
    )


TOOLS = {
    "evaluate_tei_index": {
        "description": "Calculates Left or Right Ventricular Tei Index / Myocardial Performance Index (MPI = (a - b) / b) for global systolic and diastolic cardiac evaluation.",
        "parameters": {
            "type": "object",
            "properties": {
                "interval_a_ms": {
                    "type": "number",
                    "description": "Interval from cessation to onset of inflow in ms (e.g. 390.0 ms)."
                },
                "ejection_time_et_ms": {
                    "type": "number",
                    "description": "Ventricular ejection time ET (b) in ms (e.g. 290.0 ms)."
                },
                "isovolumetric_relaxation_time_ivrt_ms": {
                    "type": "number",
                    "description": "Measured IVRT in ms, optional (e.g. 60.0 ms)."
                },
                "modality": {
                    "type": "string",
                    "description": "Doppler modality ('Pulsed Wave Doppler' or 'Tissue Doppler Imaging (TDI)'), default 'Pulsed Wave Doppler'."
                },
                "ventricle": {
                    "type": "string",
                    "description": "Chamber evaluated ('Left Ventricle' or 'Right Ventricle'), default 'Left Ventricle'."
                },
                "heart_rate_bpm": {
                    "type": "number",
                    "description": "Heart rate in beats per minute, default 72.0."
                }
            },
            "required": ["interval_a_ms", "ejection_time_et_ms"]
        },
        "handler": handle_evaluate_tei
    }
}


def process_request(request_str: str) -> str:
    try:
        req = json.loads(request_str)
        method = req.get("method")
        req_id = req.get("id")

        if method == "tools/list":
            tools_list = [
                {
                    "name": name,
                    "description": spec["description"],
                    "inputSchema": spec["parameters"]
                }
                for name, spec in TOOLS.items()
            ]
            return json.dumps({"jsonrpc": "2.0", "id": req_id, "result": {"tools": tools_list}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            if tool_name not in TOOLS:
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Tool '{tool_name}' not found"}
                })

            result = TOOLS[tool_name]["handler"](args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            })

        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32600, "message": f"Unsupported method '{method}'"}
            })

    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })


if __name__ == "__main__":
    import sys
    for line in sys.stdin:
        if line.strip():
            print(process_request(line))
            sys.stdout.flush()
