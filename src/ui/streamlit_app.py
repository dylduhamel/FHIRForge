"""
FHIRForge Streamlit UI - Clinical Notes to FHIR Converter

This Streamlit application provides a user-friendly interface for converting
clinical notes to FHIR resources using the FHIRForge API.
"""

import json
import streamlit as st
import requests
from typing import Dict, List, Any

# Page configuration
st.set_page_config(
    page_title="FHIRForge - Clinical Notes to FHIR",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Example clinical notes
EXAMPLE_NOTES = {
    "": "",
    "Type 2 Diabetes": """Patient is a 58-year-old male with type 2 diabetes mellitus.
Current medications include metformin 1000mg twice daily and glipizide 10mg daily.
HbA1c is 7.2%. Patient reports good medication compliance.
No history of diabetic complications at this time.""",

    "Hypertension & Cardiovascular": """67-year-old female with essential hypertension and coronary artery disease.
Currently taking lisinopril 20mg daily, atorvastatin 40mg nightly, and aspirin 81mg daily.
Blood pressure today is 138/82. Patient underwent cardiac catheterization last year.
Reports occasional chest discomfort with exertion.""",

    "Post-Surgery Follow-up": """Patient underwent laparoscopic cholecystectomy three weeks ago for symptomatic cholelithiasis.
Recovery has been uneventful. Surgical wounds are well-healed.
Patient is off pain medications and has resumed normal activities.
Follow-up complete, no further surgical care needed.""",

    "Respiratory & Pain Management": """42-year-old male presenting with chronic lower back pain and asthma.
Currently prescribed ibuprofen 600mg three times daily as needed for pain.
Uses albuterol inhaler for asthma symptoms. Recent X-ray showed mild degenerative changes.
Referred to physical therapy for pain management.""",
}

# API configuration
API_BASE_URL = "http://localhost:8000"

def call_conversion_api(clinical_note: str, patient_id: str = None) -> Dict[str, Any]:
    """Call the FHIRForge API to convert clinical note to FHIR"""
    try:
        payload = {"clinical_note": clinical_note}
        if patient_id:
            payload["patient_id"] = patient_id

        response = requests.post(
            f"{API_BASE_URL}/convert",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to FHIRForge API. Make sure the API is running on http://localhost:8000")
        st.info("Run the API with: `poetry run python run.py`")
        return None

    except requests.exceptions.Timeout:
        st.error("Request timed out. The API took too long to respond.")
        return None

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 422:
            try:
                error_detail = e.response.json()
                st.error("Validation Error")
                st.warning("Clinical note must be at least 10 characters long.")
                with st.expander("See detailed error"):
                    st.json(error_detail)
            except:
                st.error(f"Validation error: {e}")
        else:
            st.error(f"API error: {e}")
        return None

    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None

def highlight_entities(text: str, entities: List[Dict]) -> str:
    """Highlight entities in the original text with color coding"""
    if not entities:
        return text

    # Sort entities by start position in reverse to avoid offset issues
    sorted_entities = sorted(entities, key=lambda x: x['start'], reverse=True)

    # Color mapping for entity types
    colors = {
        'condition': '#ffcccc',  # Light red
        'medication': '#cce5ff',  # Light blue
        'procedure': '#ccffcc',   # Light green
    }

    highlighted_text = text
    for entity in sorted_entities:
        start = entity['start']
        end = entity['end']
        entity_type = entity['entity_type']
        entity_text = entity['text']
        confidence = entity['confidence']

        color = colors.get(entity_type, '#ffffcc')  # Default yellow

        # Create highlighted span
        highlight = f'<span style="background-color: {color}; padding: 2px 4px; border-radius: 3px; font-weight: 500;" title="{entity_type.title()} (confidence: {confidence:.2f})">{entity_text}</span>'

        # Replace in text
        highlighted_text = highlighted_text[:start] + highlight + highlighted_text[end:]

    return highlighted_text

def display_entity_card(entity: Dict):
    """Display a single entity as a card"""
    entity_type = entity['entity_type']
    text = entity['text']
    confidence = entity['confidence']

    # Emoji mapping
    emoji_map = {
        'condition': '🔴',
        'medication': '💊',
        'procedure': '🏥',
    }

    emoji = emoji_map.get(entity_type, '📝')

    # Color for confidence badge
    if confidence >= 0.8:
        conf_color = "green"
    elif confidence >= 0.6:
        conf_color = "orange"
    else:
        conf_color = "red"

    st.markdown(f"""
    <div style="background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin: 5px 0;">
        {emoji} <strong>{entity_type.title()}</strong>: {text}
        <span style="float: right; color: {conf_color};">●</span>
        <span style="float: right; margin-right: 10px;">{confidence:.0%}</span>
    </div>
    """, unsafe_allow_html=True)

# Main UI
st.title("🏥 FHIRForge")
st.markdown("### Clinical Notes to FHIR Converter")
st.markdown("Convert unstructured clinical notes into structured FHIR R4 resources using NLP.")

# Sidebar
with st.sidebar:
    st.header("About")
    st.markdown("""
    **FHIRForge** extracts medical entities from clinical text and generates valid FHIR resources.

    **Extracted Entities:**
    - 🔴 Conditions/Diagnoses
    - 💊 Medications
    - 🏥 Procedures

    **Output:**
    - FHIR R4 Bundle (JSON)
    - Confidence scores
    - Validation warnings
    """)

    st.divider()

    st.header("API Status")
    try:
        health_response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        if health_response.ok:
            st.success("✅ API Online")
        else:
            st.error("❌ API Error")
    except:
        st.error("❌ API Offline")
        st.caption("Start API: `poetry run python run.py`")

    st.divider()

    st.markdown("""
    **Developer Tools:**
    - [API Docs](http://localhost:8000/docs)
    - [GitHub](https://github.com/dylduhamel/fhirforge)
    """)

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Input Clinical Note")

    # Example selector
    selected_example = st.selectbox(
        "Try an example:",
        options=list(EXAMPLE_NOTES.keys()),
        help="Select a pre-filled example clinical note"
    )

    # Patient ID (optional)
    patient_id = st.text_input(
        "Patient ID (optional)",
        value="example-patient",
        help="FHIR Patient reference ID"
    )

    # Clinical note input
    clinical_note = st.text_area(
        "Clinical Note",
        value=EXAMPLE_NOTES[selected_example],
        height=300,
        placeholder="Enter clinical note here...\n\nExample:\nPatient has type 2 diabetes and hypertension.\nCurrently taking metformin 500mg BID and lisinopril 10mg daily.",
        help="Paste or type the clinical note you want to convert to FHIR"
    )

    # Convert button
    convert_button = st.button("🔄 Convert to FHIR", type="primary", use_container_width=True)

with col2:
    st.subheader("📊 Results")

    # Process conversion when button clicked
    if convert_button:
        if not clinical_note.strip():
            st.warning("⚠️ Please enter a clinical note to convert.")
        else:
            with st.spinner("Converting to FHIR..."):
                result = call_conversion_api(clinical_note, patient_id)

            if result:
                # Store in session state for persistence
                st.session_state['last_result'] = result
                st.session_state['last_note'] = clinical_note

    # Display results if available
    if 'last_result' in st.session_state:
        result = st.session_state['last_result']
        entities = result.get('entities', [])
        fhir_bundle = result.get('fhir_bundle', {})
        warnings = result.get('warnings', [])

        # Overview metrics
        st.markdown("#### Summary")
        metric_cols = st.columns(3)

        with metric_cols[0]:
            st.metric("Total Entities", len(entities))

        with metric_cols[1]:
            avg_confidence = sum(e['confidence'] for e in entities) / len(entities) if entities else 0
            st.metric("Avg Confidence", f"{avg_confidence:.0%}")

        with metric_cols[2]:
            resource_count = len(fhir_bundle.get('entry', [])) if fhir_bundle else 0
            st.metric("FHIR Resources", resource_count)

        # Tabbed interface
        tab1, tab2, tab3, tab4 = st.tabs(["📍 Highlighted Text", "📋 Entities", "🔷 FHIR Bundle", "⚠️ Validation"])

        with tab1:
            st.markdown("##### Original note with highlighted entities:")

            # Legend
            st.markdown("""
            <div style="margin-bottom: 10px;">
                <span style="background-color: #ffcccc; padding: 2px 8px; border-radius: 3px; margin-right: 10px;">Condition</span>
                <span style="background-color: #cce5ff; padding: 2px 8px; border-radius: 3px; margin-right: 10px;">Medication</span>
                <span style="background-color: #ccffcc; padding: 2px 8px; border-radius: 3px;">Procedure</span>
            </div>
            """, unsafe_allow_html=True)

            # Highlighted text
            if entities:
                highlighted_html = highlight_entities(st.session_state['last_note'], entities)
                st.markdown(
                    f'<div style="background-color: white; padding: 15px; border-radius: 5px; border: 1px solid #ddd; white-space: pre-wrap;">{highlighted_html}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.info("No entities detected in this note.")

        with tab2:
            st.markdown("##### Extracted Entities:")

            if entities:
                # Group by entity type
                entity_types = {}
                for entity in entities:
                    entity_type = entity['entity_type']
                    if entity_type not in entity_types:
                        entity_types[entity_type] = []
                    entity_types[entity_type].append(entity)

                # Display by type
                for entity_type, type_entities in entity_types.items():
                    st.markdown(f"**{entity_type.title()}s** ({len(type_entities)})")
                    for entity in type_entities:
                        display_entity_card(entity)
                    st.markdown("")
            else:
                st.info("No entities extracted from this note.")

        with tab3:
            st.markdown("##### FHIR R4 Bundle:")

            if fhir_bundle:
                # Pretty print JSON
                st.json(fhir_bundle)

                # Download button
                json_str = json.dumps(fhir_bundle, indent=2)
                st.download_button(
                    label="📥 Download FHIR Bundle (JSON)",
                    data=json_str,
                    file_name="fhir_bundle.json",
                    mime="application/json",
                    use_container_width=True
                )

                # Bundle info
                st.caption(f"Bundle type: {fhir_bundle.get('type', 'N/A')} | Resources: {len(fhir_bundle.get('entry', []))}")
            else:
                st.warning("No FHIR bundle generated.")

        with tab4:
            st.markdown("##### Validation Results:")

            if warnings:
                for warning in warnings:
                    st.warning(warning)
            else:
                st.success("✅ No validation warnings detected!")

            # Additional info
            st.info("""
            **Note:** This is a basic validation. For production use:
            - Validate against FHIR profiles (US Core, IPS)
            - Check required fields
            - Verify code systems (SNOMED CT, LOINC, RxNorm)
            - Test with FHIR validator tools
            """)
    else:
        st.info("👈 Enter a clinical note and click 'Convert to FHIR' to see results.")

# Footer
st.divider()
st.caption("FHIRForge v1.0 | Built with FastAPI + Streamlit | Phase 1.5 - Basic Web UI")