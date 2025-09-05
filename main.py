import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function
from functions.functions import available_functions
from prompts import system_prompt

def main():
    isVerbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    user_prompt = " ".join(args)

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if isVerbose:
        print(f"User prompt: {user_prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    try:
        for iteration in range(20): # Limit to 20 iterations to avoid infinite loops
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                ),
            )

            if isVerbose:
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

            if response.candidates:
                for candidate in response.candidates:
                    messages.append(candidate.content)

            if not response.function_calls:
                print("Response:")
                print(response.text)
                break

            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose=isVerbose)
                if not function_call_result.parts:
                    raise Exception("empty function call result")
                
                if isVerbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                
                function_call_result.role = "user"
                messages.append(function_call_result)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
