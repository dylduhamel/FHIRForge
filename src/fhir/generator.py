from typing import List, Dict, Any
from datetime import datetime, timezone
from fhir.resources.bundle import Bundle, BundleEntry
from fhir.resources.condition import Condition
from fhir.resources.medicationstatement import MedicationStatement
from fhir.resources.procedure import Procedure
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.codeablereference import CodeableReference
from fhir.resources.coding import Coding
from fhir.resources.reference import Reference
from src.api.models import Entity
import uuid


class FHIRGenerator:
    """Generate FHIR resources from extracted entities"""

    def __init__(self, patient_id: str = "example-patient"):
        self.patient_id = patient_id

    def generate_bundle(self, entities: List[Entity]) -> Dict[str, Any]:
        """
        Generate a FHIR Bundle from extracted entities

        :param entities: List of extracted entities

        :return: FHIR Bundle as dictionary
        """
        entries = []

        # Group entities by type
        conditions = [e for e in entities if e.entity_type == "condition"]
        medications = [e for e in entities if e.entity_type == "medication"]
        procedures = [e for e in entities if e.entity_type == "procedure"]

        # Generate Condition resources
        for condition in conditions:
            resource = self._create_condition(condition)
            entries.append(BundleEntry(
                fullUrl=f"urn:uuid:{uuid.uuid4()}",
                resource=resource
            ))

        # Generate MedicationStatement resources
        for medication in medications:
            resource = self._create_medication_statement(medication)
            entries.append(BundleEntry(
                fullUrl=f"urn:uuid:{uuid.uuid4()}",
                resource=resource
            ))

        # Generate Procedure resources
        for procedure in procedures:
            resource = self._create_procedure(procedure)
            entries.append(BundleEntry(
                fullUrl=f"urn:uuid:{uuid.uuid4()}",
                resource=resource
            ))

        bundle = Bundle(
            type="collection",
            timestamp=datetime.now(timezone.utc).astimezone().isoformat(timespec="milliseconds"),
            entry=entries if entries else None
        )

        return bundle.dict(exclude_none=True)

    def _create_condition(self, entity: Entity) -> Condition:
        """Create a FHIR Condition resource"""
        return Condition(
            id=str(uuid.uuid4()),
            clinicalStatus=CodeableConcept(
                coding=[Coding(
                    system="http://terminology.hl7.org/CodeSystem/condition-clinical",
                    code="active"
                )]
            ),
            verificationStatus=CodeableConcept(
                coding=[Coding(
                    system="http://terminology.hl7.org/CodeSystem/condition-ver-status",
                    code="confirmed"
                )]
            ),
            code=CodeableConcept(
                text=entity.text
                # TODO: Add SNOMED CT coding in future version
            ),
            subject=Reference(reference=f"Patient/{self.patient_id}"),
            recordedDate=datetime.now().isoformat()
        )

    def _create_medication_statement(self, entity: Entity) -> MedicationStatement:
        """Create a FHIR MedicationStatement resource"""
        return MedicationStatement(
            id=str(uuid.uuid4()),
            status="active",
            medication=CodeableReference(
                concept=CodeableConcept(
                    text=entity.text
                )
            ),
            subject=Reference(reference=f"Patient/{self.patient_id}"),
            dateAsserted=datetime.now().isoformat()
        )

    def _create_procedure(self, entity: Entity) -> Procedure:
        """Create a FHIR Procedure resource"""
        return Procedure(
            id=str(uuid.uuid4()),
            status="completed",
            code=CodeableConcept(
                text=entity.text
                # TODO: Add SNOMED CT coding in future version
            ),
            subject=Reference(reference=f"Patient/{self.patient_id}"),
            performedDateTime=datetime.now().isoformat()
        )


def get_generator(patient_id: str = "example-patient") -> FHIRGenerator:
    """Get FHIR generator instance"""
    return FHIRGenerator(patient_id=patient_id)