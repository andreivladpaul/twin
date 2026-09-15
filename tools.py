from agents import function_tool
from dotenv import load_dotenv

load_dotenv(override=True)

@function_tool
def record_user_details(
    email: str,
    name: str = "Name not provided",
    notes: str = "not provided",
):
    """
    Record that a user wants to be contacted.
    """

    with open("user_details.txt", "a", encoding="utf-8") as file:
        file.write(f"Name: {name}\nEmail: {email}\nNotes: {notes}\n\n")

    return "OK"
