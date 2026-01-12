"""
Pre-familiarization instructions page.
Displays introductory text before the familiarization trials begin.
"""
import streamlit as st

def show():
    """Display the pre-familiarization instructions screen."""
    st.markdown("""
    ### Welcome to the Emotion Recognition Survey!
    
    #### Please read the following instructions carefully!

    You will be shown a series of images and videos of athletes, each for 2 seconds, after which you have to answer 2 simple questions:
    """)

    st.info("""
    1. What emotions are being shown by the athlete you just saw? You can write as many emotions you think you saw, separated by commas. 
    """)
    
    st.info("""
    2. Did the athlete **win or lose** the match/contest?
    """)

    st.markdown("""
    Now, if you have understood these instructions, proceed to the **3 practice clips, followed by a message, after which your survey will begin.** 
    
    Please press start below, to begin your practice trial.
    """)

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("◀️ Back to Questionnaire", use_container_width=True):
            if st.session_state.get('confirm_back_pre_famil', False):
                st.session_state.page = 'questionnaire'
                st.session_state.user_id_confirmed = False
                st.rerun()
            else:
                st.session_state.confirm_back_pre_famil = True
                st.warning("⚠️ Click again to confirm.")

    with col3:
        if st.button("Begin Practice Trials ▶️", use_container_width=True, type="primary"):
            st.session_state.page = 'familiarization'
            st.session_state.confirm_back_pre_famil = False
            st.rerun()
