import requests
import json
import subprocess
import numpy as np
import pandas as pd
import threading
import time
# Your Wit.ai access token
access_token = "WBWNN4PCPCCALRZC4PS7SO3HOAZH23HA"

# Base URL for Wit.ai API
base_url = "https://api.wit.ai"

# Headers for API requests
headers = {
    "Authorization": f"Bearer {access_token}"
}

result = None

def run_scrapy(search_sentence):
    global result
    subprocess.run(["run_main.sh", search_sentence])
    df = pd.read_csv('test.csv')
    top_rows = df.head(5)
    messages = []

    # product_list = []

    for _, row in top_rows.iterrows():
        asin = row['asin']
        title = row['Title']
        main_image = row['MainImage']
        rating = row['Rating']
        num_reviews = row['NumberOfReviews']
        price = row['Price']
        link = f"https://www.amazon.in/dp/{asin}"

        message = f"ASIN: {asin}\nTitle: {title}\nMain Image: {main_image}\nRating: {rating}\nNumber of Reviews: {num_reviews}\nPrice: {price}\nLink: {link}"
        messages.append(message)

    final_message = "\n\n".join(messages)
    open('test.csv', 'w').close()
    result = final_message  # Convert list of dictionaries to JSON string

    


# Function to get Wit.ai API response
def get_wit_response(query):
    url = f"{base_url}/message"
    params = {"q": query}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Function to handle the response and generate bot reply
def handle_response(response):
    global result
    result = None  # Reset the result
    intents = response.get('intents', [])
    entities = response.get('entities', {})
    
    for intent in intents:
        if intent['name'] == 'Greet':
            return "Hello! How can I assist you today?"
        elif intent['name'] == 'SearchProduct':
            local_search_queries = entities.get('wit$local_search_query:local_search_query', [])
            search_sentence = ' '.join([query['body'] for query in local_search_queries])
            
            # Start a new thread to run the Scrapy script
            t = threading.Thread(target=run_scrapy, args=(search_sentence,))
            t.start()
            
            return "Sure, let me find that product for you. Please wait."
        # Add more intents here
    
    return "I'm sorry, I didn't understand that."

# Main interactive loop
# while True:
#     user_input = input("You: ")
#     if user_input.lower() == 'quit':
#         print("Bot: Goodbye!")
#         break
    
#     wit_response = get_wit_response(user_input)
#     bot_reply = handle_response(wit_response)
#     open('test.csv', 'w').close()
#     print(f"Bot: {bot_reply}")
