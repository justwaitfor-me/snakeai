from google import genai
from google.genai import types

from utils import read_file, build_prompt, get_key, parse_ai_response

def player(snake:list, opp_snake:list, food:list, grid:tuple):
    client = genai.Client(
        api_key=get_key(),
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=build_prompt(snake, opp_snake, food, grid)),
            ],
        )
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text=read_file("player.txt")),
        ],
    )
    
    part = ""

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        part += chunk.text
        
    response = parse_ai_response(part)
    
    if response != None:
        return response
    else:
        return {"error":"No Ai Output"}

if __name__ == "__main__":
    player([(5, 5), (5, 4), (5, 3)], [(10, 10), (10, 9)], [(7, 6)])