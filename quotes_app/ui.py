import streamlit as st
import pandas as pd
import plotly.express as pe
from database import create_database
# from openai import OpenAI
# from openai import AzureOpenAI

st.set_page_config(layout="wide")
rows = create_database()
# print(rows)
# print(type(rows))
# print(len(rows[0]))
# display heading and text
st.header("💬 Quotes App and Chatbot")
# form to show quote
st.subheader("Quote You Might Not Have Seen")
with st.form("display_random_quote"):
    # get quote - display "quote" - author name # call method from database
    st.subheader("methodToGetRandomQuote") 
    submitted = st.form_submit_button("Show Different Quote")
    # if submitted:
        # rerun method to get quote
quote_categories = ["Truth","Inspirational", "Life", "Humor", "Friendship", "Courage"]

# initialise table in session_state if not already initialised - so only does once
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(rows, columns=["Quote", "Author", "Tags"])
options = st.multiselect(
    "Select quote categories",
    quote_categories,
    default=quote_categories,
    on_change=None # change
)
# chosen_categories = for cat in options. 
st.write("You selected:", ", ".join(options)) # in database create database of selected category

st.subheader("Quotes")
st.dataframe(st.session_state.df, hide_index=True)


st.header("Add a Tag")
st.write("Is there a tag you think is missing and want to see more of?")

with st.form("add_tags_form"):
    #new_tags = st.multiselect("Select additional categories to see quotes of them", #method to fetch tags and s)
    search = st.form_submit_button("Add tags to select in table") 
    # if submitted:
        #quote_categories.append(new_tags)
        #reload page

st.header("Tag Distribution")
st.subheader("Current Distribution")
#  using plotly import to display chart
tags_series = st.session_state.df["Tags"].str.split(", ")
amounts = tags_series.explode().value_counts()
# amounts = st.session_state.df["Tags"]..value_counts()
chart = pe.pie(names=amounts.index, values=amounts.values)
st.plotly_chart(chart)
# most common quote tag - using pandas import functions
counts = st.session_state.df["Tags"].value_counts()
st.write("Most common tag: ", amounts.idxmax())
st.write("Number of most common tag: ", str(amounts.max()))

st.header("Search For Quotes by an Author")
with st.form("search_author_form"):
    st.text_input("Author Name and Surname", key="author")
    search = st.form_submit_button("Find Quotes By Author")
    # if submitted:
        # search quotes by author using API
        # if not empty results:
            # st.session_state.df2 = pd.DataFrame(results, columns=["Quote", "Author", "Tags"])
            # st.dataframe(st.session_state.df2, hide_index=True)
        # else 
            # st.error("Sorry couldn't find any quote by your author - please try another author")   

# Show title and description.
with st.form("chat_form"):
    st.title("💬 Chat with Quotes Guide Chatbot!")
    st.write("Tell the chatbot your current mood to generate a suitable quote:")
    prompt_bot = st.form_submit_button("Submit")

    openai_api_key = st.secrets["AZURE_OPENAI_API_KEY"]
    openai_api_endpoint = st.secrets["AZURE_OPENAI_ENDPOINT"]

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.", icon="🗝️")
    else:
        # create OpenAI client
        client = AzureOpenAI(
            api_key=openai_api_key,
            api_version="2024-12-01-preview",
            azure_endpoint=openai_api_endpoint
        )

        # store chat messages
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # display the existing chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # create a chat input field to allow the user to enter a message
        if prompt_bot:
            if prompt := st.chat_input("Hi! What are you currently feeling?"):
                # store and display current prompt
                with st.chat_message("user"):
                    st.markdown(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})  # add message to chat history

                # generate a response using the OpenAI API.
                stream = client.chat.completions.create(
                    model=st.secrets["AZURE_OPENAI_MODEL"],
                    messages=[{"role": "system", "content": "You are a friendly chatbot to validate people's feelings and provide a quote"},
                            {"role": "user", "content": prompt}],
                    stream=True
                )

                # stream the response to the chat using `st.write_stream` and then store it in session state.
                with st.chat_message("assistant"):
                    response = st.write_stream(stream)
