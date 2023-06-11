import streamlit as st
import requests

_URL = " http://127.0.0.1:8000"


def call_api_ss(query: str) -> dict:
    headers = {
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    }

    params = {
        'query': query
    }

    response = requests.post(f'{_URL}/semantic-search',
                             params=params, headers=headers)
    return response.json()


def main():
    st.title("Document Search")

    # Input search query
    search_query = st.text_input("Enter your search query:")

    # Search and display matching documents
    if search_query:
        docs_data = call_api_ss(search_query)
        if docs_data:
            st.success(f"Found {len(docs_data)} matching document(s).")
            for doc_data in docs_data:
                # Display document with collapsible section
                with st.expander(doc_data['title']):
                    st.write(doc_data['content'])
        else:
            st.warning("No matching documents found.")


if __name__ == "__main__":
    main()
