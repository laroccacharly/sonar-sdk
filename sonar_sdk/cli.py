from sonar_sdk.client import get_client
from sonar_sdk.display_response import display_response
from sonar_sdk.sonar_request import SonarRequest, SonarModels

from openai.types.chat.chat_completion import ChatCompletion
import argparse
from pathlib import Path
import sys
import os

def send_request(request: SonarRequest) -> ChatCompletion:
    client = get_client()
    messages = request.get_messages()
    print(f"Sending request to {request.model.value}")
    response: ChatCompletion = client.chat.completions.create(
        model=request.model.value,
        messages=messages,
    )
    return response

def main():
    parser = argparse.ArgumentParser(description="Sonar CLI - Interact with Sonar models")
    parser.add_argument("-m", "--model", type=int, default=1, choices=range(1, 6),
                        help="Model selection (1-5): 1=SONAR (default/smallest), 2=SONAR_PRO, "
                             "3=SONAR_REASONING, 4=SONAR_REASONING_PRO, 5=SONAR_DEEP_RESEARCH (largest)")
    parser.add_argument("-f", "--file", type=str,
                        help="Path to a prompt file (optional, if not provided, prompt must be given as positional argument)")
    parser.add_argument("-s", "--system-prompt", type=str,
                        default="You are a helpful assistance that can answer questions.",
                        help="System prompt to use")
    parser.add_argument("--no-save", action="store_true",
                        help="Don't save the response to a file")
    parser.add_argument("prompt", nargs="*", help="The prompt text (if not using a file)")
    
    args = parser.parse_args()
    
    # If saving responses, inform user about the save location
    if not args.no_save:
        search_history_path = os.environ.get("SEARCH_HISTORY_PATH")
        if search_history_path:
            save_dir = Path(search_history_path)
            print(f"Responses will be saved to: {save_dir}")
        else:
            print("Responses will be saved to: ./responses/")
    
    # Map model number to SonarModels enum
    model_map = {
        1: SonarModels.SONAR,  # smallest
        2: SonarModels.SONAR_PRO,
        3: SonarModels.SONAR_REASONING,
        4: SonarModels.SONAR_REASONING_PRO,
        5: SonarModels.SONAR_DEEP_RESEARCH  # largest
    }
    
    selected_model = model_map[args.model]
    
    # Handle prompt input
    prompt_text = None
    prompt_path = None
    
    if args.file:
        # Use file as prompt source
        prompt_path = Path(args.file)
    elif args.prompt:
        # Use command line argument as prompt
        prompt_text = " ".join(args.prompt)
    else:
        print("Error: No prompt provided. Please provide a prompt as an argument or use -f to specify a prompt file.")
        sys.exit(1)
    
    # Create a custom SonarRequest that can handle direct prompt text
    request = SonarRequest(
        model=selected_model,
        system_prompt=args.system_prompt,
        save_response=not args.no_save
    )
    
    # Set the prompt text or path
    if prompt_path:
        request.prompt_path = prompt_path
    else:
        # Use the prompt_text field
        request.prompt_text = prompt_text
    
    response = send_request(request)
    display_response(response, save_to_file=request.save_response)

if __name__ == "__main__":
    main() 