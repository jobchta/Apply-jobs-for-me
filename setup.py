import json

def run_setup():
    """
    Runs an interactive setup process to create the config.json file.
    """
    print("--- Wells Fargo Job Application Bot Setup ---")
    print("This script will guide you through configuring the bot.")
    print("Please provide the following information:")

    # --- Credentials ---
    email = input("Enter your Wells Fargo careers login email: ")

    # --- Job URLs ---
    job_urls = []
    print("\\nEnter the URLs of the jobs you want to apply for.")
    print("Press Enter after each URL. When you are finished, just press Enter on an empty line.")
    while True:
        url = input("Job URL: ")
        if not url:
            break
        job_urls.append(url)

    # --- File Paths ---
    print("\\nEnter the full paths to the following files:")
    chromedriver_path = input("Path to your chromedriver executable: ")
    resume_path = input("Path to your resume PDF file: ")

    # --- Build the config dictionary ---
    # We will use the detailed profile info from the original script
    config = {
        "job_urls": job_urls,
        "credentials": {
            "email": email
        },
        "profile": {
            "email": "rahulkotian269@gmail.com",
            "legal_name": "Rahul Ravindra Kotian",
            "address": "53, Kalpana, Shree Mahalakshmi Chs Ltd, Veera Desai Road, Andheri West, Mumbai-400058, Maharashtra, India",
            "phone": "+91 91671 22112",
            "compensation": "1200000",
            "citizenship": "India",
            "gender": "Male",
            "how_heard": "Wells Fargo Careers Website",
            "prev_wf_employee": "No",
            "preferred_name": "No",
            "current_cell": "Personal Cell",
            "nation": "India"
        },
        "work_experience": [
            {
                "job_title": "Data Analyst (Trainee Software Programmer)",
                "company": "Marlabs LLC",
                "location": "Syracuse, NY, USA",
                "current": "No",
                "from": "05/2024",
                "to": "02/2025",
                "description": "Developed comprehensive Power BI dashboards..."
            }
        ],
        "education": [
            {
                "school": "Syracuse University",
                "degree": "M.S.",
                "field": "Management Information Systems",
                "gpa": "3.67"
            }
        ],
        "languages": [
            {
                "language": "English",
                "fluency": "Fluent",
                "reading": "3 - Fluent",
                "speaking": "3 - Fluent",
                "writing": "3 - Fluent"
            }
        ],
        "app_questions": {
            "desired_compensation": "1200000",
            "wf_employee": "No",
            "sponsorship_required": "No",
            "non_compete": "No",
            "fiduciary_appointments": "No",
            "board_member": "No",
            "other_work": "No",
            "ownership_interest": "No",
            "business_control": "No",
            "government_position": "No",
            "political_campaign": "No",
            "family_relationship": "No",
            "kpmg_employee": "No"
        },
        "vol_dis": {
            "citizenship_status": "Citizen (India)",
            "nationality": "India",
            "gender": "Male"
        },
        "paths": {
            "chromedriver": chromedriver_path,
            "resume": resume_path
        }
    }

    # --- Save the config file ---
    try:
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)
        print("\\nConfiguration saved successfully to config.json!")
        print("You can now run the bot with: python3 apply_bot.py")
    except IOError as e:
        print(f"\\nError: Could not save the configuration file. {e}")

if __name__ == "__main__":
    run_setup()
