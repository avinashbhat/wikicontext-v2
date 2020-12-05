import streamlit as st
from src.wikicontext import WikiContext
import json
import os, urllib
import wikipedia
import nltk


def main():
    st.sidebar.title('WikiContext')

    # Download external dependencies
    download_title = st.text('Downloading dependencies...')
    for filename in external_dependencies.keys():
        download_file(filename)
    if download_title is not None:
        download_title.empty()
    nltk.download('stopwords')
    nltk.download('punkt')
    # Algorithm Selection
    algorithm = True
    algorithm = st.sidebar.selectbox("Algorithm that you want to use.", ["TextRank", "T5"], index=0)

    if algorithm == "T5":
        t5_model = st.sidebar.selectbox("Select a T5 Model.", ["T5 Small"], index=0)
        run_t5_algorithm(t5_model)
    if algorithm == "TextRank":
        run_the_app(algorithm)


def download_file(file_path):
    # Don't download the file twice. (If possible, verify the download using the file length.)
    if os.path.exists(file_path):
        if "size" not in external_dependencies[file_path]:
            return
        elif os.path.getsize(file_path) == external_dependencies[file_path]["size"]:
            return

    # These are handles to two visual elements to animate.
    weights_warning, progress_bar = None, None
    try:
        weights_warning = st.warning("Downloading %s..." % file_path)
        progress_bar = st.progress(0)
        with open(file_path, "wb") as output_file:
            with urllib.request.urlopen(external_dependencies[file_path]["url"]) as response:
                length = int(response.info()["Content-Length"])
                counter = 0.0
                MEGABYTES = 2.0 ** 20.0
                while True:
                    data = response.read(8192)
                    if not data:
                        break
                    counter += len(data)
                    output_file.write(data)

                    # We perform animation by overwriting the elements.
                    weights_warning.warning("Downloading %s... (%6.2f/%6.2f MB)" %
                                            (file_path, counter / MEGABYTES, length / MEGABYTES))
                    progress_bar.progress(min(counter / length, 1.0))

    # Finally, we remove these visual elements by calling .empty().
    finally:
        if weights_warning is not None:
            weights_warning.empty()
        if progress_bar is not None:
            progress_bar.empty()


def run_t5_algorithm(t5_model):
    params = {}  # This will hold the hyper parameters for the summarizers
    if t5_model == "T5 Small":
        params['model'] = "models/t5-small/"
        params['tokenizer'] = "models/t5-small/"
    run_the_app("T5", params)


def run_the_app(algorithm, params=None):
    if params is None:
        params = {}

    query = st.text_input(label="The topic you want summarized.", value="")
    results = []
    if query:
        results = wikipedia.search(query)
        subject = st.selectbox(label="Choose the Wikipedia page.", options=results, index=0)

        if subject and algorithm:
            wc = WikiContext(subject, algorithm, params)
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
def get_search_results(wikicontext):
    if not wikicontext.subject:
        return
    return wikicontext.get_search_results()


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
    with open('models/model_meta.json') as config_file:
        external_dependencies = json.load(config_file)
    main()
