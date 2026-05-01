import streamlit as st
import pandas as pd
import plotly.express as pe
from database import create_database
# from openai import OpenAI
# from openai import AzureOpenAI

rows = create_database()
print(rows)
print(type(rows))
print(len(rows[0]))
# display heading and text
st.header("💬 Quotes App and Chatbot 💬")
# form to show quote
with st.form("display_random_quote"):
    st.subheader("Quote You Might Like")
    # get quote - display "quote" - author name # call method from database
    st.subheader("methodToGetRandomQuote") 
    submitted = st.form_submit_button("Show Different Quote")
    # if submitted:
        # rerun method to get quote
quote_categories = ["Truth","Inspirational", "Life", "Humor", "Friendship", "Courage"]

# initialise table in session_state if not already initialised - so only does once
if "df" not in st.session_state:

    st.session_state.df = pd.DataFrame(rows, columns=["Quote", "Author", "Tags"])
# st.subheader("My Quotes")
# if "df2" not in st.session_state:
    # st.session_state.df2 = pd.DataFrame(rows, columns=["Quote", "Author", "Tags"])
# form to add personal quote
# with st.form("user_added_quotes"):
#     st.text_input("Quote", key="quote")
#     st.text_input("Author", key="author")
#     st.selectbox("Tags", key="tags", options=quote_categories)

    # button to caused newly added guest to be processed
    # submitted = st.form_submit_button("Add Quote to My List")
    # if submitted:
    #     # validate input - cannot be empty
    #     if (st.session_state.name and st.session_state.dish):
    #         new_row = pd.DataFrame({
    #             "ID": [len(st.session_state.df) + 1],
    #             "Quote": [st.session_state.quote],
    #             "Author": [st.session_state.author],
    #             "Tags": [st.session_state.tags]
    #         })
    #         # preserve data between reruns
    #         st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
    #     else:
    #         st.error("Fields may not be empty - please fill in missing value(s)")

st.subheader("Quotes")
st.dataframe(st.session_state.df, hide_index=True)

# second section
st.header("🥇 Dish Types")

# most common dish type info - using pandas import functions
counts = st.session_state.df["Dish Type"].value_counts()
st.write("Most catered type of dish: ", counts.idxmax())
st.write("Number of most catered dish type: ", str(counts.max()))

st.header("🍽️ Dish Type Distribution")
st.subheader("Current Distribution")
#  using plotly import to display chart
amounts = st.session_state.df["Dish Type"].value_counts()
chart = pe.pie(names=amounts.index, values=amounts.values)
st.plotly_chart(chart)


st.set_page_config(layout="wide")
# Show title and description.
with st.form("chat_form"):
    st.title("💬 Chat with Pesach Meal Prep Chatbot!")
    st.write("Ask the chatbot for a dish suggestion:")
    prompt_bot = st.form_submit_button("Get Suggestion")

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
            if prompt := st.chat_input("Hi! I am ready to assist with your Pesach meal prep - how's it going?"):
                # store and display current prompt
                with st.chat_message("user"):
                    st.markdown(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})  # add message to chat history

                # generate a response using the OpenAI API.
                stream = client.chat.completions.create(
                    model=st.secrets["AZURE_OPENAI_MODEL"],
                    messages=[{"role": "system", "content": "You are a friendly chatbot helping guests pick a Passover Seder dish."},
                            {"role": "user", "content": prompt}],
                    stream=True
                )

                # stream the response to the chat using `st.write_stream` and then store it in session state.
                with st.chat_message("assistant"):
                    response = st.write_stream(stream)
