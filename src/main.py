from subject import Subject

import streamlit as st

st.title('WikiContext')

subject = st.text_input(label="The Wikipedia page that you want summarized.", 
                    value="")

if subject:
    subject = Subject(subject)
    summary = subject.get_summary()
    page = subject.get_page_content()
    st.markdown(summary)
    st.markdown(page)