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
    # Use backend directory for CSV storage (works in both local and Render)
    from pathlib import Path
    backend_dir = Path(__file__).parent.parent.parent.parent
    csv_path = backend_dir / "user_contacts.csv"
    file_exists = csv_path.exists()
    
    # Ensure parent dir exists
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Name", "Email", "Organization", "Message"])
        writer.writerow([name, email, organization, message])
    return {"status": "success", "message": "Details saved successfully"}


