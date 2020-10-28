from src.subject import Subject
from src.algorithms.textrank import TextRank
from src.algorithms.transformer import Transformer
from src.utils import format_dict_to_text
import streamlit as st


# [TEMP] Placeholder for the prerequisite dict.
prerequisite_dict={
    "Luminosity": "Luminosity can also be given in terms of the astronomical magnitude system: the absolute bolometric magnitude (Mbol) of an object is a logarithmic measure of its total energy emission rate, while absolute magnitude is a logarithmic measure of the luminosity within some specific wavelength range or filter band.",
    "Dark Matter": "In the standard Lambda-CDM model of cosmology, the total mass–energy of the universe contains 5% ordinary matter and energy, 27% dark matter and 68% of a form of energy known as dark energy. Thus, dark matter constitutes 85% of total mass, while dark energy plus dark matter constitute 95% of total mass–energy content.Because dark matter has not yet been observed directly, if it exists, it must barely interact with ordinary baryonic matter and radiation, except through gravity.",
    "String Theory": "In string theory, one of the many vibrational states of the string corresponds to the graviton, a quantum mechanical particle that carries gravitational force. Because string theory potentially provides a unified description of gravity and particle physics, it is a candidate for a theory of everything, a self-contained mathematical model that describes all fundamental forces and forms of matter. Subsequently, it was realized that the very properties that made string theory unsuitable as a theory of nuclear physics made it a promising candidate for a quantum theory of gravity."
}

def main():
    st.sidebar.title('WikiContext')

    algorithm = st.sidebar.selectbox("Algorithm that you want to use.", ["TextRank", "BART", "T5"], index=0)

    if algorithm == "T5":
        t5_model = st.sidebar.selectbox("Select a T5 Model.", ["T5 Base", "T5 Small"], index=0)
        if t5_model == "T5 Base":
            t5_model = "t5-base"
        elif t5_model == "T5 Small":
            t5_model = "t5-small"

    subject = st.text_input(label="The Wikipedia page that you want summarized.", value="")

    if subject and algorithm:
        subject = Subject(subject)
        summary = subject._get_summary()
        if algorithm == "TextRank":
            summary = get_textrank_summary(summary)
        elif algorithm == "BART":
            summary = get_bart_summary(summary)
        elif algorithm == "T5":
            summary = get_t5_summary(summary, t5_model)
        else:
            summary = "Algorithm is not implemented.."
        st.header("Summary")
        st.markdown(summary)

        st.header("Prerequisites")
        format_dict_to_text(prerequisite_dict)



@st.cache
def get_textrank_summary(wiki_summary):
    return TextRank(wiki_summary).get_summary()


@st.cache
def get_bart_summary(wiki_summary):
    return Transformer(wiki_summary).get_bart_summary(min_length=40, max_length=150)


@st.cache
def get_t5_summary(wiki_summary):
    return Transformer(wiki_summary).get_t5_summary(model=t5_model, tokenizer=t5_model, framework="tf",
                                                    min_length=40, max_length=150)

if __name__ == "__main__":
    main()