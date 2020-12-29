import streamlit as st
from src.wikicontext import WikiContext
import wikipedia


def main():
    st.sidebar.title('WikiContext')
    algorithm = st.sidebar.selectbox("Algorithm that you want to use.", ["TextRank", "BERT"], index=0)

    max_prereqs = st.sidebar.slider("How many prerequisites do you want to see?", min_value=2, max_value=10)

    ratio = st.sidebar.slider("How verbose do you want your summary to be?", min_value=1, max_value=10, value=2)

    params = {'ratio': ratio/10}

    if algorithm:
        if algorithm == "BERT":
            algorithm = "Bert"
    run_the_app(algorithm, params=params, max_prereqs=max_prereqs)


def run_the_app(algorithm, params=None, max_prereqs=5):
    if params is None:
        params = {}

    query = st.text_input(label="The topic you want summarized.", value="")
    results = []
    if query:
        results = wikipedia.search(query)
        subject = st.selectbox(label="Choose from disambiguation.", options=results, index=0)

        if subject and algorithm:
            wc = WikiContext(subject, algorithm, params, max_prereqs=max_prereqs)
            st.title(subject)
            with st.spinner(text="Generating summary..."):
                st.markdown(get_main_summary(wc))
            with st.spinner(text="Generating prerequisites..."):
                prereqs = get_prereq_summary(wc)
            st.header("Prerequisites")
            for subhead in prereqs:
                st.subheader(subhead)
                st.write(prereqs[subhead])


@st.cache(show_spinner=False)
def get_main_summary(wikicontext):
    if not wikicontext.content:
        wikicontext.get_main_content()
    return wikicontext.get_main_summary()


@st.cache(show_spinner=False)
def get_prereq_summary(wikicontext):
    if not wikicontext.prereq:
        wikicontext.get_prereqs_content()
    return wikicontext.get_prereqs_summary()


if __name__ == "__main__":
    main()
