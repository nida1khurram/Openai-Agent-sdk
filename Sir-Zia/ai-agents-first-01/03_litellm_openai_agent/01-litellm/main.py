# type: ignore
from litellm import completion
import os

os.environ["OPEN_ROUTER_KEY"] = OPEN_ROUTER_KEY
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

def openai():
    response = completion(
        model="openai/gpt-4o",
        messages=[{ "content": "Hello, how are you?","role": "user"}]
    )

    print(response)

def gemini():
    response = completion(
        model="gemini/gemini-1.5-flash",
        messages=[{ "content": "Hello, how are you?","role": "user"}]
    )

    print(response)

def gemini2():
    response = completion(
        model="gemini/gemini-2.0-flash-exp",
        messages=[{ "content": "Hello, how are you?","role": "user"}]
    )

    print(response)


# #type:ignore
# from litellm import completion
# from dotenv import load_dotenv  # type: ignore
# import os

# # Load environment variables from .env file
# load_dotenv()

# #  models
# #model 1 openai
# def openai(user_input):
#     response = completion(
#         model="openrouter/openai/gpt-4o",
#         messages=[{"role": "user", "content": user_input}],
#         max_tokens=200
#     )
#     print(response.choices[0].message.content)

# #model 2 gemini
# def gemini(user_input):
#     response = completion(
#         model="gemini/gemini-1.5-flash",
#         messages=[{"role": "user", "content": user_input}],
#         max_tokens=200
#     )
#     print(response.choices[0].message.content)

# #model 3 mistral
# def mistral(user_input):
#     response = completion(
#         model="openrouter/mistral/mistral-7b-instruct",
#         messages=[{"role": "user", "content": user_input}],
#         max_tokens=200
#     )
#     print(response.choices[0].message.content)


# # Main logic
# if __name__ == "__main__":
#     choice = input("Choose model (openai / gemini / mistral): ").lower()

#     if choice in ["openai", "gemini", "mistral"]:
#         user_input = input("Enter your query: ")

#         if choice == "openai":
#             openai(user_input)
#         elif choice == "gemini":
#             gemini(user_input)
#         elif choice == "mistral":
#             mistral(user_input)
#     else:
#         print("Invalid choice.")