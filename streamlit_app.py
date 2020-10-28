import streamlit as st
from src.wikicontext import WikiContext

@st.cache
def get_main_summary(wikicontext):
    return wikicontext.get_main_summary()

@st.cache
def get_prereq_summary(wikicontext):
    return wikicontext.get_prereq_summary()

def main():
    st.sidebar.title('WikiContext')
    algorithm = True
    # algorithm = st.sidebar.selectbox("Algorithm that you want to use.", ["TextRank", "BART", "T5"], index=0)

    # if algorithm == "T5":
    #     t5_model = st.sidebar.selectbox("Select a T5 Model.", ["T5 Base", "T5 Small"], index=0)
    #     if t5_model == "T5 Base":
    #         t5_model = "t5-base"
    #     elif t5_model == "T5 Small":
    #         t5_model = "t5-small"

    subject = st.text_input(label="The Wikipedia page that you want summarized.", value="")

    if subject and algorithm:
        wc = WikiContext(subject, algorithm)
        st.title(subject)
        st.markdown(get_main_summary(wc))
        prereqs = get_prereq_summary(wc)
        st.header("Prerequisites")
        for subhead in prereqs:
            st.subheader(subhead)
            st.write(prereqs[subhead])



# @st.cache
# def get_textrank_summary(wiki_summary):
#     return TextRank(wiki_summary).get_summary()


# @st.cache
# def get_bart_summary(wiki_summary):
#     return Transformer(wiki_summary).get_bart_summary(min_length=40, max_length=150)


# @st.cache
# def get_t5_summary(wiki_summary):
#     return Transformer(wiki_summary).get_t5_summary(model=t5_model, tokenizer=t5_model, framework="tf",
#                                                     min_length=40, max_length=150)

if __name__ == "__main__":
    main()