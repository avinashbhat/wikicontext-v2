import streamlit as st
from src.wikicontext import WikiContext

@st.cache
def get_main_summary(wikicontext):
    if not wikicontext.content:
        wikicontext.get_main_content()
    return wikicontext.get_main_summary()


@st.cache
def get_prereq_summary(wikicontext):
    if not wikicontext.prereq:
        wikicontext.get_prereqs_content()
    return wikicontext.get_prereqs_summary()


def main():
    st.sidebar.title('WikiContext')
    algorithm = True
    params = {}  # This will hold the hyperparameters for the summarizers
    algorithm = st.sidebar.selectbox("Algorithm that you want to use.", ["TextRank", "BART", "T5"], index=0)

    if algorithm == "T5":
        t5_model = st.sidebar.selectbox("Select a T5 Model.", ["T5 Base", "T5 Small"], index=0)
        if t5_model == "T5 Base":
            params['model'] = "t5-base"
            params['tokenizer'] = "t5-base"
        elif t5_model == "T5 Small":
            params['model'] = "t5-small"
            params['tokenizer'] = "t5-small"

    subject = st.text_input(label="The Wikipedia page that you want summarized.", value="")

    if subject and algorithm:
        wc = WikiContext(subject, algorithm, params)
        st.title(subject)
        st.markdown(get_main_summary(wc))
        prereqs = get_prereq_summary(wc)
        st.header("Prerequisites")
        for subhead in prereqs:
            st.subheader(subhead)
            st.write(prereqs[subhead])


if __name__ == "__main__":
    main()
