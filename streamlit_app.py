import streamlit as st
from src.wikicontext import WikiContext
import wikipedia


def main():
    st.sidebar.title('WikiContext')
    algorithm = st.sidebar.selectbox("Algorithm that you want to use.", ["TextRank"], 
        index=0)

    max_prereqs = st.sidebar.slider("How many prerequisites do you want to see?", min_value=2, 
        max_value=10)

    if algorithm == "TextRank":
        run_the_app(algorithm, max_prereqs=max_prereqs)

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

def run_the_app(algorithm, params=None, max_prereqs=5):
    if params is None:
        params = {}

    query = st.text_input(label="The topic you want summarized. For best results, paste the exact page title from Wikipedia.", value="")
    results = []
    if query:
        results = wikipedia.search(query)
        if not results:
            st.markdown("No such page found!")
        else:
            query = results[0]
        if query and algorithm and results:
            wc = WikiContext(query, algorithm, params, max_prereqs=max_prereqs)
            try:
                with st.spinner(text="Generating summary..."):
                    main_summary = get_main_summary(wc)
                        
                with st.spinner(text="Generating prerequisites..."):
                    prereqs = get_prereq_summary(wc)
                st.title(query)
                st.markdown(main_summary)
                st.header("Prerequisites")
                for subhead in prereqs:
                    st.subheader(subhead)
                    st.write(prereqs[subhead])
            except ValueError as ve:
                results.remove(query)
                query = st.selectbox(label="Please choose from disambiguation.", 
                    options=results, index=0)


if __name__ == "__main__":
    main()
