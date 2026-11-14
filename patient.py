from fhir.resources.patient import Patient
from fhir.resources.humanname import HumanName
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.identifier import Identifier
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding

# Crear el recurso FHIR de paciente con parámetros opcionales
def create_patient_resource(family_name=None, given_name=None, birth_date=None, gender=None, phone=None, document_number=None):
    patient = Patient()

    # Agregar el documento como identifier si está disponible
    if document_number:
        identifier = Identifier()
        identifier.use = "official"
        identifier.system = "http://www.renaper.gob.ar/dni"  # URI del organismo emisor (ej. RENAPER en Argentina)
        identifier.value = str(document_number)
        
        # Especificar el tipo de identificador según estándar HL7 (NNARG = National Person Identifier Argentina, o PPN / DL / MR)
        coding = Coding()
        coding.system = "http://terminology.hl7.org/CodeSystem/v2-0203"
        coding.code = "NNARG"
        coding.display = "National Person Identifier Argentina"
        
        codeable_concept = CodeableConcept()
        codeable_concept.coding = [coding]
        identifier.type = codeable_concept
        
        patient.identifier = [identifier]
    
    # Agregar el nombre del paciente si está disponible
    if family_name or given_name:
        name = HumanName()
        if family_name:
            name.family = family_name
        if given_name:
            name.given = [given_name]
        patient.name = [name]
    
    # Agregar la fecha de nacimiento si está disponible
    if birth_date:
        patient.birthDate = birth_date

    # Agregar el género si está disponible
    if gender:
        patient.gender = gender

    # Agregar información de contacto si está disponible
    if phone:
        contact = ContactPoint()
        contact.system = "phone"
        contact.value = phone
        contact.use = "mobile"
        patient.telecom = [contact]

    return patient