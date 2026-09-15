from dotenv import load_dotenv

import gradio as gr

from agents import Runner

from agent import digital_twin

async def chat(message, history):

    result = await Runner.run(
        digital_twin,
        message,
    )

    return result.final_output

    
if __name__ == "__main__":

    gr.ChatInterface(
        fn=chat,
        title="Digital Twin",
        description="Talk to my AI twin",
    ).launch(server_name="0.0.0.0", server_port=7860)