import requests
from patient import create_patient_resource
import json
import requests

# Enviar el recurso FHIR al servidor HAPI FHIR
def send_resource_to_hapi_fhir(resource, resource_type):
    url = f"https://hapi.fhir.org/baseR4/{resource_type}"
    headers = {
        "Content-Type": "application/fhir+json; charset=utf-8",
        "Accept": "application/fhir+json"
    }

    # Serializar a JSON string y codificar a UTF-8 para evitar cortes con acentos ("ó", "á", etc.)
    json_payload = resource.model_dump_json().encode("utf-8")

    response = requests.post(url, headers=headers, data=json_payload)

    if response.status_code in (200, 201):
        created_resource = response.json()
        resource_id = created_resource.get("id")
        print(f"Recurso {resource_type} creado exitosamente con ID: {resource_id}")
        return resource_id
    else:
        print(f"Error al crear el recurso: {response.status_code}")
        print(response.json())
        return None

# Buscar el recurso por ID 
def get_resource_from_hapi_fhir(resource_id, resource_type):
    url = f"https://hapi.fhir.org/baseR4/{resource_type}/{resource_id}"
    response = requests.get(url, headers={"Accept": "application/fhir+json"})

    if response.status_code == 200:
        resource = response.json()
        print(resource)
    else:
        print(f"Error al obtener el recurso: {response.status_code}")
        print(response.json())

def search_patient_by_identifier(document_number, system=None):
    url = "https://hapi.fhir.org/baseR4/Patient"
    
    # En FHIR, si se incluye system, el formato es "system|value"; si no, solo "value"
    if system:
        params = {"identifier": f"{system}|{document_number}"}
    else:
        params = {"identifier": str(document_number)}

    response = requests.get(url, headers={"Accept": "application/fhir+json"}, params=params)

    if response.status_code == 200:
        bundle = response.json()
        entries = bundle.get("entry", [])
        
        if not entries:
            print(f"No se encontraron pacientes con el documento: {document_number}")
            return []
        
        print(f"Se encontraron {len(entries)} paciente(s):")
        patients = []
        for entry in entries:
            patient_resource = entry["resource"]
            patients.append(patient_resource)
            print(json.dumps(patient_resource, indent=2))
            
        return patients
    else:
        print(f"Error al buscar el paciente: {response.status_code}")
        print(response.json())
        return []
    