from src.subject import Subject
from src.algorithms.textrank import TextRank
from src.algorithms.pipeline import Pipeline
from src.algorithms.t5 import T5

import streamlit as st

st.title('WikiContext')

algorithm = st.selectbox("Algorithm that you want to use.", ["TextRank", "Pipeline API", "T5"], index=0)

subject = st.text_input(label="The Wikipedia page that you want summarized.", value="")


@st.cache
def get_textrank_summary(summary):
    # Move this function to wikicontext file 
    return TextRank(summary).get_summary()

@st.cache
def get_pipeline_summary(summary):
    return Pipeline(summary).get_summary()

@st.cache
def get_t5_summary(summary):
    return T5(summary).get_summary()


if subject and algorithm:
    subject = Subject(subject)
    summary = subject._get_summary()
    if algorithm == "TextRank":
        summary = get_textrank_summary(summary)
    elif algorithm == "Pipeline API":
        summary = get_pipeline_summary(summary)
    elif algorithm == "T5":
        summary = get_t5_summary(summary)
    else:
        summary = "Algorithm is not implemented.."
    st.markdown(summary)
