"""
Contact endpoint for storing user submissions.
"""

from fastapi import APIRouter, Form
import csv
import os

router = APIRouter()


@router.post("/contact")
async def save_contact(
    name: str = Form(...),
    email: str = Form(...),
    organization: str = Form(""),
    message: str = Form("")
):
    csv_path = os.path.join(os.getcwd(), "user_contacts.csv")
    file_exists = os.path.exists(csv_path)
    # Ensure parent dir exists
    os.makedirs(os.path.dirname(csv_path) or ".", exist_ok=True)
    with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Name", "Email", "Organization", "Message"])
        writer.writerow([name, email, organization, message])
    return {"status": "success", "message": "Details saved successfully"}


