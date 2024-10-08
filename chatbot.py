import wikipediaapi
import re
import operator
import random
import datetime

# Initialize Wikipedia API with a user agent
wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent='ChatBot/1.0 (Contact: reaganm746@gmail.com)'  # Replace with your email
)

# Predefined responses for basic conversation
conversational_responses = {
    "hello": ["Hi there!", "Hello! How can I help you today?", "Hey! What's up?"],
    "how are you": ["I'm just a bot, but I'm doing great!", "I'm good, thanks! How about you?", "All systems running smoothly!"],
    "what's your name": ["I'm your friendly chatbot, but you can call me Bro!", "You can call me Bro."],
    "bye": ["Goodbye!", "Talk to you later!", "Bye! Have a great day!"],
    "which is the best team": ["Manchester United"],
    "when was manchester united founded": ["1878"],
}

# Function to perform calculations
def calculate(expression):
    ops = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}
    expression = re.sub(r'[^0-9+\-*/.]', '', expression)  # Clean the input
    for op in ops:
        if op in expression:
            left, right = expression.split(op)
            return ops[op](float(left), float(right))  # Perform the calculation
    return "I can only do basic calculations."

# Function for Wikipedia search
def wiki_search(query):
    # Directly check the query for more straightforward responses
    page = wiki_wiki.page(query)
    if page.exists():
        return page.summary[:500]  # Return the first 500 characters of the summary

    # If the direct search fails, use common variations
    variations = [
        f"{query} (disambiguation)",
        f"{query} geography",
        f"{query} history",
        f"{query} culture",
        f"{query} location",
    ]

    for variant in variations:
        page = wiki_wiki.page(variant)
        if page.exists():
            return page.summary[:500]  # Return first 500 characters of summary

    # Fallback descriptions for common locations
    if query.lower() == "kenya":
        return "Kenya is located in East Africa and is known for its diverse wildlife and landscapes."
    elif query.lower() in ["america", "united states", "usa"]:
        return "America, or the United States, is a country primarily located in North America, known for its diverse geography and cultural influence."

    return "I couldn't find that on Wikipedia. Please try another question."

# Functions for time and date
def get_current_time():
    now = datetime.datetime.now()
    return now.strftime("The current time is %H:%M:%S")

def get_current_date():
    today = datetime.datetime.now()
    return today.strftime("Today's date is %Y-%m-%d")

# Handle basic conversation
def handle_conversation(user_input):
    user_input = user_input.lower()  # Make input case-insensitive

    for key in conversational_responses:
        if key in user_input:
            return random.choice(conversational_responses[key])  # Pick a random response
    
    return None  # If no match is found

# Main response function
def chatbot_response(user_input):
    user_input = user_input.lower()

    # Handle basic conversation
    conversation_reply = handle_conversation(user_input)
    if conversation_reply:
        return conversation_reply

    # Handle time request
    if "time" in user_input:
        return get_current_time()

    # Handle date request
    if "date" in user_input:
        return get_current_date()

    # Handle calculations
    if "calculate" in user_input:
        expression = re.findall(r'calculate (.+)', user_input)
        if expression:
            return calculate(expression[0])
        else:
            return "Please provide a valid calculation."

    # Handle Wikipedia search for common topics or general input
    return wiki_search(user_input)

# Create the main chat loop
def chat():
    print("Hello! I'm Bro, your assistant. Ask me anything!")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Bro: Goodbye!")
            break
        response = chatbot_response(user_input)
        print(f"Bro: {response}")

if __name__ == "__main__":
    chat()
