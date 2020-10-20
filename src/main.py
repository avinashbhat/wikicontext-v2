import streamlit as st 
import wikipedia
st.title('WikiContext')

search_keyword = st.text_input(label="The Wikipedia page that you want summarized.", 
                    value="Portmanteau")
if search_keyword:
    summary = wikipedia.summary(search_keyword)
    st.markdown(summary)