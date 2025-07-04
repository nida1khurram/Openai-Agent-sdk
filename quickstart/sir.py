#type:ignore
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic import BaseModel
import requests
import asyncio

# Load environment variables
load_dotenv()

# Gemini API Configuration
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in .env file")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Define a model for guardrail output
class KiaCommandOutput(BaseModel):
    is_valid_command: bool
    reasoning: str

# Guardrail function to validate Kia-related commands
def kia_command_guardrail(user_input: str) -> KiaCommandOutput:
    valid_commands = ["lock vehicle", "unlock vehicle", "check location", "check battery"]
    user_input_lower = user_input.lower()

    if any(command in user_input_lower for command in valid_commands):
        return KiaCommandOutput(
            is_valid_command=True,
            reasoning="Valid Kia vehicle command."
        )
    else:
        return KiaCommandOutput(
            is_valid_command=False,
            reasoning="Invalid or off-topic command."
        )

# Kia API interaction function (simulated using Smartcar API)
def kia_api_lock_vehicle(access_token: str, vehicle_id: str):
    # Simulated API call to lock a vehicle (replace with actual Smartcar API call)
    url = f"https://api.smartcar.com/v2.0/vehicles/{vehicle_id}/security"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(url, json={"action": "LOCK"}, headers=headers)
    return response.json()

# Async function to process user input with Gemini model
async def process_kia_command(user_input: str, access_token: str, vehicle_id: str):
    # Apply guardrail
    guardrail_result = kia_command_guardrail(user_input)
    if not guardrail_result.is_valid_command:
        print(f"Guardrail blocked the request: {guardrail_result.reasoning}")
        return

    # If guardrail passes, query Gemini model
    try:
        response = await external_client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[
                {"role": "system", "content": "You are a Kia vehicle assistant. Handle commands like lock/unlock vehicle or check location."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150
        )
        gemini_response = response.choices[0].message.content
        print("Gemini Response:", gemini_response)

        # If the command involves vehicle action, call Kia API
        if "lock vehicle" in user_input.lower():
            api_response = kia_api_lock_vehicle(access_token, vehicle_id)
            print("API Response:", api_response)
        else:
            print("Command processed but no API action required.")

    except Exception as e:
        print(f"Error querying Gemini API: {str(e)}")

# Main function to run the async code
async def main():
    access_token = "<your-access-token>"  # Replace with actual Smartcar access token
    vehicle_id = "<your-vehicle-id>"      # Replace with actual vehicle ID

    # Test cases
    print("Test 1: Valid command")
    await process_kia_command("Lock vehicle", access_token, vehicle_id)

    print("\nTest 2: Invalid command")
    await process_kia_command("Do my math homework", access_token, vehicle_id)

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())