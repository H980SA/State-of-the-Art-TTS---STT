from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv  
load_dotenv()
import os
import asyncio

model = ChatOpenAI(model="gpt-4o-mini-2024-07-18")
template = "eres un comediante y di algo gracioso sobre {topic}, sé lo más coloquial posible sin uso de ** o ## o -"
prompt_template = ChatPromptTemplate.from_messages(
    [("system", template), ("user", "{topic}")]
)
parser = StrOutputParser()
chain = prompt_template | model | parser

# Create an async function with customizable chunk size
async def stream_joke(topic, min_words=4):
    """
    Stream a joke about a topic with customizable minimum words per chunk.
    
    Args:
        topic: The subject of the joke
        min_words: Minimum number of words per chunk (default: 4)
    """
    # Buffer to accumulate text
    buffer = ""
    word_count = 0
    
    # Process the stream
    async for event in chain.astream_events({"topic": topic}):
        kind = event["event"]
        if kind == "on_chat_model_stream":
            # Get the new chunk of text
            new_text = event["data"]["chunk"].content
            buffer += new_text
            
            # Count words in buffer (simple split-based counting)
            current_words = len(buffer.split())
            
            # Process if we have enough words
            if current_words >= min_words:
                print('| ' + buffer, end="", flush=True)
                
                # Process the chunk here (in a real app, you'd send to TTS)
                # process_chunk(buffer)
                
                # Reset buffer
                buffer = ""
    
    # Process any remaining text in the buffer
    if buffer.strip():
        print('| ' + buffer, end="", flush=True)
        # process_chunk(buffer)
        
    print()  # Add newline at end

# Run the async function
if __name__ == "__main__":
    print("Generating a joke about parrots...\n")
    asyncio.run(stream_joke("parrot", min_words=4))