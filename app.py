from src.subject import Subject
from src.algorithms.textrank import TextRank

import streamlit as st

st.title('WikiContext')

algorithm = st.selectbox("Algorithm that you want to use.", ["TextRank", "T5"], index=0)

subject = st.text_input(label="The Wikipedia page that you want summarized.", 
                    value="")

@st.cache
def get_textrank_summary(summary):
    # Move this function to wikicontext file 
    return TextRank(summary).get_summary()


if subject and algorithm:
    subject = Subject(subject)
    if algorithm == "TextRank":
        summary = subject._get_summary()
        summary = get_textrank_summary(summary)
    else:
        summary = "Algorithm is not implemented.."
    st.markdown(summary)