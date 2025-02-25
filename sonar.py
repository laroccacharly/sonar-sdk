from client import get_client
from display_response import display_response
from sonar_request import SonarRequest

from openai.types.chat.chat_completion import ChatCompletion

def send_request(request: SonarRequest) -> ChatCompletion:
    client = get_client()
    messages = request.get_messages()
    print(f"Sending request to {request.model.value}")
    response: ChatCompletion = client.chat.completions.create(
        model=request.model.value,
        messages=messages,
    )
    return response

if __name__ == "__main__":
    request = SonarRequest()
    response = send_request(request)
    display_response(response, save_to_file=request.save_response) 
