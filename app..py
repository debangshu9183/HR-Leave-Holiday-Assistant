from src.pdf_loader import extract_pdf_text
from src.csv_database import load_csv_to_db
from src.prompt import build_prompt
from src.groq_client import create_client, MODEL
from src.chatbot import chat_with_hr

PDF_PATH = r"F:\\HR_chatbot\\data\\Leave Details.pdf"
CSV_PATH = r"F:\HR_chatbot\data\Holiday_List_2026.csv"
import os

print(os.listdir("data"))

leave_policy_text = extract_pdf_text(PDF_PATH)


df, connection = load_csv_to_db(CSV_PATH)

system_prompt = build_prompt(leave_policy_text)

client = create_client()

print("=" * 55)
print("  HR Assistant (Leave Policy + Holiday List) 🤖")
print("  Powered by Groq  |  Type 'exit' to quit")
print("=" * 55)

conversation_history = []

while True:

    user_input = input("\nYou: ").strip()

    if user_input.lower() in ("exit", "quit", "q"):
        print("Goodbye! 👋")
        break

    answer = chat_with_hr(
        user_input,
        conversation_history,
        client,
        MODEL,
        system_prompt,
        connection
    )

    print(f"\n🤖 Assistant: {answer}")