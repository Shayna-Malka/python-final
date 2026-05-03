import streamlit as st
import pandas as pd
import plotly.express as pe
from database import create_databases, add_tags_to_database, extract_data_from_tagged_db, add_data_to_databases, extract_data_from_untagged_db
from web_scraping import scrape
from api import api_request_random_quote
import time
# from openai import OpenAI
# from openai import AzureOpenAI
# explain in readme why tag request is created - bec if refer to chart a lot of clutter so chose a few
st.set_page_config(layout="wide")
if "quote_categories" not in st.session_state: 
    # default categories for quotes - user can add to them
    st.session_state.quote_categories = ["truth","inspirational", "life", "friendship", "courage"]
create_databases()
add_tags_to_database(st.session_state.quote_categories)
add_data_to_databases()

if "random_quote" not in st.session_state:
    st.session_state.random_quote = api_request_random_quote()
st.header("💬 Quotes App and Chatbot")
# form to show quote
st.subheader("Quote You Might Not Have Seen")
with st.form("display_random_quote"):
    # get quote - display "quote" and author name - call method from database
    random_quote = st.session_state.random_quote
    st.subheader(f'"{st.session_state.random_quote["quote"]}"') 
    st.write(f"-{st.session_state.random_quote["author"]}")
    submitted = st.form_submit_button("Show Different Quote")
    if submitted:
        st.session_state.random_quote = api_request_random_quote()


# initialise table in session_state if not already initialised - so only does once
# if "df" not in st.session_state:


st.subheader("Quotes")
quote_tags_or_without = st.radio(
    "Select quotes categorisation",
    ["Only categorised quotes", "Only uncategorised quotes", "Both"]
)
if quote_tags_or_without == "Only categorised quotes":
    # st.session_state.df = pd.DataFrame(rows, columns=["Quote", "Author", "Tags"])
    st.session_state.options_selected = st.multiselect(
    "Select quote categories",
    [q.capitalize() for q in st.session_state.quote_categories],
    default=[q.capitalize() for q in st.session_state.quote_categories],
    on_change=None # change
)
# chosen_categories = for cat in options. 
    st.write("You selected:", ", ".join(st.session_state.options_selected)) # in database create database of selected category
    rows = extract_data_from_tagged_db(st.session_state.options_selected)
    st.session_state.df = pd.DataFrame(rows, columns=["Quote", "Author", "Tags"])

if quote_tags_or_without == "Only uncategorised quotes":
    rows = extract_data_from_untagged_db()
    st.session_state.df = pd.DataFrame(rows, columns=["Quote", "Author"])

if quote_tags_or_without == "Both":
    rows = extract_data_from_tagged_db()
    rows += [(q, a, "") for q, a in extract_data_from_untagged_db()]
    st.session_state.df = pd.DataFrame(rows, columns=["Quote", "Author", "Tags"])

st.dataframe(st.session_state.df)  #, hide_index=True)

if quote_tags_or_without == "Only categorised quotes":
    st.header("Add a Tag")
    st.write("Is there a tag you think is missing and want to see more of?")
    with st.form("add_tags_form"):
        user_requested_category= st.text_input(
        "Request a quote category",
        placeholder="e.g. comedy, failure, hope",
        help="Type a category. If it exists, you can use it to filter quotes in above table.")
        add = st.form_submit_button("Add Category")  # in readme: add that if category is not a lot and might be connected to other category then might not refelect change in table
        if add:
            #check if not in category already
            requested_cat = user_requested_category.lower().strip()
            if requested_cat not in st.session_state.quote_categories:
                print("NOT IN")
                results, _ =scrape(f"tag/{user_requested_category.lower().strip()}/")
                if len(results)>0:
                    st.session_state.quote_categories.append(requested_cat)
                    add_tags_to_database(requested_cat)
                    st.success("Category added successfully! Please wait a few moments for page to update")
                    time.sleep(4)
                    st.rerun()
                else:
                    st.error("Sorry your category is not included as a tag in the website - please try another category")
            else:
                st.error("Category is already included - please choose a a category that is not listed in red above table with quotes") 

    st.header("Tag Distribution")
    st.subheader("Current Distribution")
    #  using plotly import to display chart
    tags_categories = st.session_state.df["Tags"].str.split(", ")
    amounts = tags_categories.explode().value_counts()
    # amounts = st.session_state.df["Tags"]..value_counts()
    chart = pe.pie(names=amounts.index, values=amounts.values)
    st.plotly_chart(chart)
    # most common quote tag - using pandas import functions
    counts = st.session_state.df["Tags"].value_counts()
    st.write("Most common tag: ", amounts.idxmax()) # include in docs that won't change with pie chart changes
    st.write("Number of most common tag: ", str(amounts.max()))

st.header("Search For Quotes by an Author")
with st.form("search_author_form"):
    st.text_input("Author Name and Surname", key="author")
    search = st.form_submit_button("Find Quotes By Author")
    if submitted:
        # search quotes by author using API
        result = 
        # if not empty results:
            # st.session_state.df2 = pd.DataFrame(results, columns=["Quote", "Author"])
            # st.dataframe(st.session_state.df2, hide_index=True)
        # else 
            # st.error("Sorry couldn't find any quote by your author - please try another author")   

# Show title and description.
# with st.form("chat_form"):
#     st.title("💬 Chat with Quotes Guide Chatbot!")
#     st.write("Tell the chatbot your current mood to generate a suitable quote:")
#     prompt_bot = st.form_submit_button("Submit")

#     openai_api_key = st.secrets["AZURE_OPENAI_API_KEY"]
#     openai_api_endpoint = st.secrets["AZURE_OPENAI_ENDPOINT"]

#     if not openai_api_key:
#         st.info("Please add your OpenAI API key to continue.", icon="🗝️")
#     else:
#         # create OpenAI client
#         client = AzureOpenAI(
#             api_key=openai_api_key,
#             api_version="2024-12-01-preview",
#             azure_endpoint=openai_api_endpoint
#         )

#         # store chat messages
#         if "messages" not in st.session_state:
#             st.session_state.messages = []

#         # display the existing chat messages
#         for message in st.session_state.messages:
#             with st.chat_message(message["role"]):
#                 st.markdown(message["content"])

#         # create a chat input field to allow the user to enter a message
#         if prompt_bot:
#             if prompt := st.chat_input("Hi! What are you currently feeling?"):
#                 # store and display current prompt
#                 with st.chat_message("user"):
#                     st.markdown(prompt)
#                 st.session_state.messages.append({"role": "user", "content": prompt})  # add message to chat history

#                 # generate a response using the OpenAI API.
#                 stream = client.chat.completions.create(
#                     model=st.secrets["AZURE_OPENAI_MODEL"],
#                     messages=[{"role": "system", "content": "You are a friendly chatbot to validate people's feelings and provide a quote"},
#                             {"role": "user", "content": prompt}],
#                     stream=True
#                 )

#                 # stream the response to the chat using `st.write_stream` and then store it in session state.
#                 with st.chat_message("assistant"):
#                     response = st.write_stream(stream)
