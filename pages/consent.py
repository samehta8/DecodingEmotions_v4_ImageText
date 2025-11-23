"""
Consent page - Participant information and consent form.
"""
import streamlit as st

def show():
    """Display the consent screen."""
    st.title("📋 Participant Information and Consent")

    st.markdown("---")

    # Participant Information
    st.markdown("""
    ## Study Information

    Thank you for your interest in participating in this research study. Before you proceed,
    please read the following information carefully.

    ### Purpose of the Study

    This study aims to collect subjective ratings of video content to better understand
    emotional responses and perceptions. Your participation will contribute to research
    in the field of emotion recognition and human perception.

    ### What Will Happen During the Study

    - You will complete a brief demographic questionnaire
    - You will watch a series of short video clips
    - You will rate each video using provided rating scales
    - The entire study should take approximately 20-30 minutes

    ### Data Usage and Privacy

    **Your data will be:**
    - Processed completely **anonymously** for research purposes
    - Used only for academic research and scientific publications
    - **Not shared with third parties** outside the research team
    - Stored securely with access restricted to authorized researchers

    **Your identity:**
    - Your responses will be linked only to an anonymous user ID
    - Your name and email will be stored separately from your ratings
    - No personally identifiable information will be included in published results

    ### Your Rights

    - **Voluntary Participation**: Your participation is completely voluntary
    - **Right to Withdraw**: You may terminate your participation at any time without
      giving a reason and without any negative consequences
    - **Questions**: You may contact the study administration at any time if you have questions
    - **Follow-up Contact**: You may be contacted via the email address you provided
      if we have follow-up questions about your responses

    ### Risks and Benefits

    - **Risks**: There are no known risks associated with participation in this study
    - **Benefits**: Your participation will contribute to scientific understanding in this field

    ### Contact Information

    If you have any questions about this study, please contact the study administration
    at the email address provided to you.
    """)

    st.markdown("---")

    # Consent Section
    st.markdown("## Consent Declaration")

    st.markdown("""
    By checking the box below, you confirm that:

    1. You have read and understood the participant information above
    2. You consent to participate in this research study voluntarily
    3. You understand that your participation is voluntary and you may withdraw at any time
    4. You consent to the processing of your data anonymously for research purposes
    5. You understand that your data will not be shared with third parties
    6. You consent to being contacted via email for potential follow-up questions
    7. You are at least 18 years old
    """)

    # Consent checkbox
    consent_given = st.checkbox(
        "**I have read and understood the information above, and I consent to participate in this study**",
        key="consent_checkbox"
    )

    st.markdown("")
    st.markdown("")

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("◀️ Back", use_container_width=True):
            st.session_state.page = 'login'
            st.rerun()

    with col3:
        if st.button("Next ▶️", use_container_width=True, type="primary"):
            if not consent_given:
                st.error("⚠️ You must provide your consent to proceed with the study.")
                st.stop()
            else:
                # Store consent in session state with timestamp
                from datetime import datetime
                st.session_state.consent_given = True
                st.session_state.consent_timestamp = datetime.now().isoformat(timespec='seconds')
                st.session_state.page = 'questionnaire'
                st.rerun()
