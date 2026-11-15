from fhir.resources.R4B.allergyintolerance import AllergyIntolerance, AllergyIntoleranceReaction
from fhir.resources.R4B.codeableconcept import CodeableConcept
from fhir.resources.R4B.coding import Coding
from fhir.resources.R4B.reference import Reference


def create_allergy_resource(
    patient_id,
    substance_code="764146007",
    substance_display="Alergia a la penicilina",
    category="medication",
    criticality="high",
    manifestation_code="271807003",
    manifestation_display="Erupción cutánea (rash)",
    severity="moderate"
):
    # 1. Crear primero la referencia obligatoria al paciente
    patient_ref = Reference(reference=f"Patient/{patient_id}")

    # 2. Instanciar AllergyIntolerance (R4) pasando el campo obligatorio 'patient'
    allergy = AllergyIntolerance(patient=patient_ref)

    # 3. Estado clínico (active / inactive / resolved)
    clinical_coding = Coding(
        system="http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
        code="active",
        display="Active"
    )
    allergy.clinicalStatus = CodeableConcept(coding=[clinical_coding])

    # 4. Estado de verificación (confirmed / unconfirmed / presumed)
    verification_coding = Coding(
        system="http://terminology.hl7.org/CodeSystem/allergyintolerance-verification",
        code="confirmed",
        display="Confirmed"
    )
    allergy.verificationStatus = CodeableConcept(coding=[verification_coding])

    # 5. Tipo, categoría y criticidad (en R4 'type' es str)
    allergy.type = "allergy"
    allergy.category = [category]
    allergy.criticality = criticality

    # 6. Sustancia causante (usando terminología SNOMED CT)
    substance_coding = Coding(
        system="http://snomed.info/sct",
        code=substance_code,
        display=substance_display
    )
    allergy.code = CodeableConcept(coding=[substance_coding], text=substance_display)

    # 7. Detalle de la reacción adversa
    if manifestation_display:
        manifestation_coding = Coding(
            system="http://snomed.info/sct",
            code=manifestation_code,
            display=manifestation_display
        )
        manifestation = CodeableConcept(coding=[manifestation_coding], text=manifestation_display)
        
        reaction = AllergyIntoleranceReaction(
            manifestation=[manifestation],
            severity=severity
        )
        allergy.reaction = [reaction]

    return allergy
