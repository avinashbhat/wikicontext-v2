from src.subject import Subject
from src.algorithms.textrank import TextRank
from src.algorithms.transformer import Transformer

import streamlit as st

st.title('WikiContext')

algorithm = st.selectbox("Algorithm that you want to use.", ["TextRank", "BART", "T5"], index=0)

if algorithm == "T5":
    t5_model = st.selectbox("Select a T5 Model.", ["T5 Base", "T5 Small"], index=0)
    if t5_model == "T5 Base":
        t5_model = "t5-base"
    else:
        t5_model = "t5-small"

subject = st.text_input(label="The Wikipedia page that you want summarized.", value="")


@st.cache
def get_textrank_summary(wiki_summary):
    # Move this function to wikicontext file 
    return TextRank(wiki_summary).get_summary()

@st.cache
def get_bart_summary(wiki_summary):
    return Transformer(wiki_summary).get_bart_summary(min_length=40, max_length=150)

@st.cache
def get_t5_summary(wiki_summary):
    return Transformer(wiki_summary).get_t5_summary(model=t5_model, tokenizer=t5_model, framework="tf",
                                                    min_length=40, max_length=150)


if subject and algorithm:
    subject = Subject(subject)
    summary = subject._get_summary()
    if algorithm == "TextRank":
        summary = get_textrank_summary(summary)
    elif algorithm == "Bart":
        summary = get_bart_summary(summary)
    elif algorithm == "T5":
        summary = get_t5_summary(summary)
    else:
        summary = "Algorithm is not implemented.."
    st.markdown(summary)
