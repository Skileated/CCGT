"""
Contact endpoint for storing user submissions.
"""

from fastapi import APIRouter, Form, HTTPException
import csv
import os
import logging
from pathlib import Path

router = APIRouter()
logger = logging.getLogger(__name__)


def get_csv_path():
    """Get the path to the user_contacts.csv file."""
    # Try multiple methods to find the backend directory
    # Method 1: Relative to this file (works in local development)
    try:
        backend_dir = Path(__file__).parent.parent.parent.parent
        csv_path = backend_dir / "user_contacts.csv"
        # Verify we're in the right place by checking for app directory
        if (backend_dir / "app").exists():
            return csv_path
    except Exception as e:
        logger.warning(f"Method 1 failed: {e}")
    
    # Method 2: Use current working directory (works in production)
    try:
        cwd = Path.cwd()
        # Check if we're in backend directory
        if (cwd / "app").exists():
            csv_path = cwd / "user_contacts.csv"
            return csv_path
        # Check if we're in project root
        if (cwd / "backend" / "app").exists():
            csv_path = cwd / "backend" / "user_contacts.csv"
            return csv_path
    except Exception as e:
        logger.warning(f"Method 2 failed: {e}")
    
    # Method 3: Use absolute path from app directory
    try:
        # Find app directory by looking for main.py
        app_dir = Path(__file__).parent.parent.parent
        backend_dir = app_dir.parent
        csv_path = backend_dir / "user_contacts.csv"
        return csv_path
    except Exception as e:
        logger.warning(f"Method 3 failed: {e}")
    
    # Fallback: Use current directory
    return Path("user_contacts.csv").resolve()


@router.get("/contact/status")
async def get_contact_status():
    """Check if the CSV file exists and is accessible."""
    try:
        csv_path = get_csv_path()
        exists = csv_path.exists()
        readable = csv_path.is_file() and os.access(csv_path, os.R_OK)
        writable = csv_path.parent.exists() and os.access(csv_path.parent, os.W_OK)
        
        info = {
            "csv_path": str(csv_path),
            "csv_path_absolute": str(csv_path.resolve()),
            "exists": exists,
            "readable": readable,
            "writable": writable,
            "parent_dir": str(csv_path.parent),
            "parent_exists": csv_path.parent.exists(),
            "parent_writable": csv_path.parent.exists() and os.access(csv_path.parent, os.W_OK),
        }
        
        if exists:
            try:
                stat = csv_path.stat()
                info["file_size"] = stat.st_size
                info["last_modified"] = stat.st_mtime
            except Exception as e:
                info["file_stat_error"] = str(e)
        
        return {"status": "ok", **info}
    except Exception as e:
        logger.error(f"Error checking contact status: {e}", exc_info=True)
        return {"status": "error", "error": str(e)}


@router.post("/contact")
async def save_contact(
    name: str = Form(...),
    email: str = Form(...),
    organization: str = Form(...),
    message: str = Form(...)
):
    """Save contact form submission to CSV file."""
    try:
        csv_path = get_csv_path()
        logger.info(f"CSV file path: {csv_path}")
        logger.info(f"CSV file absolute path: {csv_path.resolve()}")
        
        file_exists = csv_path.exists()
        logger.info(f"CSV file exists: {file_exists}")
        
        # Ensure parent directory exists
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write to CSV file
        try:
            with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["Name", "Email", "Organization", "Message"])
                    logger.info("Created new CSV file with headers")
                writer.writerow([name, email, organization, message])
                logger.info(f"Successfully wrote contact: {name} ({email})")
        except PermissionError as e:
            logger.error(f"Permission denied writing to CSV: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Cannot write to CSV file: Permission denied. Path: {csv_path}"
            )
        except IOError as e:
            logger.error(f"IO error writing to CSV: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Cannot write to CSV file: {str(e)}. Path: {csv_path}"
            )
        
        return {"status": "success", "message": "Details saved successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error saving contact: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error saving contact: {str(e)}"
        )


