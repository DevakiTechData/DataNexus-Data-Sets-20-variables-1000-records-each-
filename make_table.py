import argparse, os, random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from faker import Faker

SEED = 20251021
random.seed(SEED); np.random.seed(SEED)
fake = Faker("en_US")

N = 1000
YMIN, YMAX = 2015, 2025

majors = ["Computer Science","Information Systems","Data Science","Cybersecurity",
          "Business Analytics","Software Engineering","Electrical Engineering",
          "Finance","Marketing","Biostatistics"]
degrees = ["BS","BA","MS","MBA","PhD"]
industries = ["Technology","Finance","Healthcare","Consulting","Education","Retail",
              "Manufacturing","Government","Non-Profit","Energy"]
roles = ["Software Engineer","Data Analyst","Data Engineer","Business Analyst","QA Engineer",
         "SDET","Product Manager","DevOps Engineer","ML Engineer","Security Analyst",
         "Salesforce Developer"]
techs = ["Python","Java","JavaScript","SQL","AWS","Azure","GCP","Snowflake","Tableau",
         "Power BI","Docker","Kubernetes","React","Node.js",".NET","C++","R","Spark","Hadoop"]
job_portals = ["LinkedIn","Handshake","Indeed","Company Site","Referral","Glassdoor","Campus Career Fair"]
event_types = ["Career Fair","Workshop","Seminar","Hackathon","Alumni Meetup","Webinar","Employer Info Session"]
states = ["MO","IL","CA","TX","NY","MA","WA","FL","CO","NC","AZ","GA","OH","PA","MI"]
cities_by_state = {
    "MO":["St. Louis","Kansas City","Columbia","Springfield","Chesterfield","Clayton"],
    "IL":["Chicago","Springfield","Urbana","Naperville","Peoria"],
    "CA":["San Francisco","San Jose","Los Angeles","San Diego","Irvine"],
    "TX":["Austin","Dallas","Houston","San Antonio","Plano"],
    "NY":["New York","Buffalo","Rochester","Albany","White Plains"],
    "MA":["Boston","Cambridge","Worcester","Somerville"],
    "WA":["Seattle","Bellevue","Redmond","Tacoma"],
    "FL":["Miami","Orlando","Tampa","Jacksonville"],
    "CO":["Denver","Boulder","Colorado Springs","Fort Collins"],
    "NC":["Raleigh","Charlotte","Durham","Cary"],
    "AZ":["Phoenix","Tempe","Scottsdale","Tucson"],
    "GA":["Atlanta","Alpharetta","Savannah"],
    "OH":["Columbus","Cleveland","Cincinnati"],
    "PA":["Philadelphia","Pittsburgh","Harrisburg"],
    "MI":["Detroit","Ann Arbor","Grand Rapids"],
}
domains = ["techcorp.com","finvista.com","healthplus.org","consultex.com","edulabs.edu",
           "retailmax.com","manufab.io","govservices.gov","greenenergy.co","nonprofit.org"]

def city_state():
    st = random.choice(states)
    return random.choice(cities_by_state[st]), st

def rand_date(y0=YMIN, y1=YMAX):
    start = datetime(y0,1,1); end = datetime(y1,12,31)
    return (start + timedelta(days=random.randint(0,(end-start).days))).date().isoformat()

def join_nonempty(items, k): return ", ".join(random.sample(items, k=k))

def ensure_no_nulls(df, name):
    assert df.shape == (1000, 20), f"{name} must be 1000x20 (got {df.shape})"
    assert not df.isnull().values.any(), f"{name} has NULLs"
    empties = (df.astype(str).apply(lambda s: s.str.strip() == "")).any().any()
    assert not empties, f"{name} has empty strings"

# ---------------- makers ----------------
def make_employers():
    rows=[]
    for i in range(1,N+1):
        company = fake.unique.company().replace(",","")
        city, state = city_state()
        rows.append({
            "Employer_ID": i,
            "Company_Name": company,
            "Industry": random.choice(industries),
            "City": city,
            "State": state,
            "Country": "USA",
            "Partnership_Level": random.choice(["Prospect","Bronze","Silver","Gold","Strategic"]),
            "Contact_Name": fake.name(),
            "Contact_Email": f"hr@{random.choice(domains)}",
            "Contact_Phone": fake.phone_number(),
            "Website": f"https://{company.replace(' ','').lower()}.com",
            "Company_Size": random.choice(["1-50","51-200","201-1k","1k-5k","5k+"]),
            "NAICS_Code": f"{random.randint(111110, 928120)}",
            "Address_Line1": fake.street_address(),
            "Address_Line2": f"Suite {random.randint(100,999)}",
            "Zip_Code": fake.zipcode(),
            "Partnership_Start_Date": rand_date(2015, 2025),
            "Active_Flag": random.choice(["Yes","No"]),
            "Remote_Policy": random.choice(["Onsite","Hybrid","Remote"]),
            "Diversity_Program": random.choice(["Yes","No"])
        })
    df = pd.DataFrame(rows); ensure_no_nulls(df,"employers"); df.to_csv("employers.csv", index=False)

def make_alumni():
    rows=[]
    for i in range(1,N+1):
        fn, ln = fake.first_name(), fake.last_name()
        city, state = city_state()
        grad_year = random.randint(YMIN, YMAX)
        years_since = 2025 - grad_year
        if years_since <= 0:
            phase = "CPT"
        elif years_since == 1:
            phase = random.choice(["OPT","CPT"])
        elif years_since <= 3:
            phase = random.choice(["OPT","STEM-OPT"])
        else:
            phase = "Full-Time"
        rows.append({
            "Alumni_ID": i,
            "First_Name": fn,
            "Last_Name": ln,
            "SLU_Email": f"{fn.lower()}.{ln.lower()}{random.randint(1,999)}@slu.edu",
            "Personal_Email": f"{fn.lower()}.{ln.lower()}{random.randint(1,999)}@{random.choice(['gmail.com','outlook.com','yahoo.com'])}",
            "Degree": random.choice(degrees),
            "Major": random.choice(majors),
            "Graduation_Year": grad_year,
            "Visa_Phase": phase,
            "City": city,
            "State": state,
            "Country": "USA",
            "Current_Employer_ID": random.randint(1,N),
            "Current_Role": random.choice(roles),
            "Current_Technologies": join_nonempty(techs, k=random.choice([1,2,3])),
            "Employment_Type": random.choice(["Full-Time","Contract","Intern","Part-Time"]),
            "Salary_USD": int(np.clip(np.random.normal(100_000, 20_000), 45_000, 230_000)),
            "Job_Portal_Source": random.choice(job_portals),
            "LinkedIn_URL": f"https://www.linkedin.com/in/{fn.lower()}{ln.lower()}{random.randint(100,999)}",
            "Zip_Code": fake.zipcode()
        })
    df = pd.DataFrame(rows)
    ensure_no_nulls(df,"alumni")
    df.to_csv("alumni.csv", index=False)

def make_students():
    assert os.path.exists("employers.csv"), "students requires employers.csv"
    rows=[]
    programs = ["MS Information Systems","MS Computer Science","MBA","MS Data Science","MS Cybersecurity","MS Analytics","MS Software Engineering"]
    for i in range(1,N+1):
        fn, ln = fake.first_name(), fake.last_name()
        city, state = city_state()
        enroll = random.randint(2018, 2024)
        exp_grad = enroll + random.choice([1,2,3])
        emp_id = random.randint(1,N)  # always present to avoid nulls
        start = rand_date(enroll, exp_grad)
        rows.append({
            "Student_ID": i,
            "First_Name": fn,
            "Last_Name": ln,
            "SLU_Email": f"{fn.lower()}.{ln.lower()}{random.randint(1,999)}@slu.edu",
            "Program": random.choice(programs),
            "Major": random.choice(majors),
            "Enrollment_Year": enroll,
            "Expected_Graduation_Year": exp_grad,
            "Visa_Status": random.choice(["F1","CPT","OPT","STEM-OPT"]),
            "Enrollment_Status": random.choice(["Full-Time","Part-Time"]),
            "GPA": round(np.clip(np.random.normal(3.4,0.4), 2.0, 4.0),2),
            "Credits_Earned": int(np.clip(np.random.normal(24,12), 0, 60)),
            "Advisor_Name": fake.name(),
            "City": city,
            "State": state,
            "Country": "USA",
            "Current_Employer_ID": emp_id,  # FK (always present)
            "Internship_Role": random.choice(["Data Analyst Intern","Software Intern","QA Intern","Research Assistant","DevOps Intern"]),
            "Internship_Start_Date": start,
            "Student_Roll_Number": f"SLU{random.randint(100000,999999)}"
        })
    df = pd.DataFrame(rows)
    ensure_no_nulls(df,"students")
    # FK sanity
    emp = pd.read_csv("employers.csv")
    assert df["Current_Employer_ID"].isin(emp["Employer_ID"]).all()
    df.to_csv("students.csv", index=False)

def make_events():
    rows=[]
    for i in range(1,N+1):
        etype = random.choice(event_types)
        city, state = city_state()
        date = rand_date(2015, 2025)
        start_time = f"{random.randint(8,18):02d}:{random.choice([0,15,30,45]):02d}"
        capacity = random.randint(30, 400); attendees = random.randint(10, capacity)
        rows.append({
            "Event_ID": i,
            "Event_Name": f"{etype} {fake.word().capitalize()}",
            "Event_Type": etype,
            "Organizer": random.choice(["SLU Career Services","SLU Alumni Association","Employer Relations","CS Dept","Business School","External Employer"]),
            "Event_Date": date,
            "Category": random.choice(["University","Employer"]),
            "Location_City": city,
            "Location_State": state,
            "Location_Country": "USA",
            "Start_Time": start_time,
            "Duration_Minutes": str(random.choice([60,90,120,180])),
            "Modality": random.choice(["In-Person","Virtual","Hybrid"]),
            "Registration_Required": "Yes",
            "Capacity": str(capacity),
            "Attendees_Actual": str(attendees),
            "Sponsor": random.choice(["SLU","IEEE","ACM","Company Partner","Graduate School"]),
            "Cost_USD": str(random.choice([0,10,25,50])),
            "Feedback_Average": f"{round(np.clip(np.random.normal(4.2,0.6),1.0,5.0),2)}",
            "Department": random.choice(["Engineering","Business","Analytics","Career Services"]),
            "Notes": random.choice(["Great turnout","Targeted to MS students","Tech-focused","Networking-heavy"])
        })
    df = pd.DataFrame(rows); ensure_no_nulls(df,"events"); df.to_csv("events.csv", index=False)

def make_jobs():
    assert os.path.exists("alumni.csv") and os.path.exists("employers.csv"), "jobs requires alumni.csv + employers.csv"
    alumni_df = pd.read_csv("alumni.csv"); employers_df = pd.read_csv("employers.csv")
    rows=[]
    for i in range(1,N+1):
        alum_id = random.randint(1,N); emp_id = random.randint(1,N)
        grad = int(alumni_df.loc[alum_id-1, "Graduation_Year"])
        start_year = max(grad-1, 2015)
        start_date = rand_date(start_year, 2025)
        end_year = max(int(start_date[:4]), 2016)
        end_date = rand_date(end_year, 2025)
        city, state = city_state()
        rows.append({
            "Job_ID": i,
            "Alumni_ID": alum_id,
            "Employer_ID": emp_id,
            "Role": random.choice(roles),
            "Technology": join_nonempty(techs, k=random.choice([1,2,3])),
            "Employment_Type": random.choice(["Full-Time","Contract","Intern","Part-Time"]),
            "Work_Auth_At_Hire": random.choice(["CPT","OPT","STEM-OPT","H1B","Citizen"]),
            "Remote_Flag": random.choice(["Yes","No"]),
            "City": city,
            "State": state,
            "Country": "USA",
            "Start_Date": start_date,
            "End_Date": end_date,
            "Job_Portal": random.choice(job_portals),
            "Salary_USD": str(int(np.clip(np.random.normal(100_000, 22_000), 45_000, 230_000))),
            "Bonus_USD": str(int(np.clip(np.random.normal(7_500, 3_000), 0, 25_000))),
            "Performance_Rating": str(random.randint(1,5)),
            "Manager_Name": fake.name(),
            "Team": random.choice(["Platform","Data","QA","SRE","Security","Apps"]),
            "Offer_Accept_Days": str(int(np.clip(np.random.normal(10,5),1,45)))
        })
    df = pd.DataFrame(rows); ensure_no_nulls(df,"jobs"); 
    # FK sanity
    assert df["Alumni_ID"].isin(alumni_df["Alumni_ID"]).all()
    assert df["Employer_ID"].isin(employers_df["Employer_ID"]).all()
    df.to_csv("jobs.csv", index=False)

def make_engagements():
    assert os.path.exists("alumni.csv") and os.path.exists("events.csv"), "engagements requires alumni.csv + events.csv"
    alumni_df = pd.read_csv("alumni.csv"); events_df = pd.read_csv("events.csv")
    rows=[]
    for i in range(1,N+1):
        alum_id = random.randint(1,N); evt_id = random.randint(1,N)
        rows.append({
            "Engagement_ID": i,
            "Alumni_ID": alum_id,
            "Event_ID": evt_id,
            "Participation_Score": str(int(np.clip(np.random.normal(80, 15), 20, 100))),
            "Feedback_Text": random.choice([
                "Great networking opportunity","Informative session","Helpful for interviews",
                "Met potential employers","Good alumni connections","Relevant content","Average experience"
            ]),
            "Checkin_Method": random.choice(["QR","Manual","Kiosk"]),
            "Attendance_Status": random.choice(["Attended","No-Show","Cancelled"]),
            "Feedback_Rating": str(random.randint(1,5)),
            "Survey_Completed": random.choice(["Yes","No"]),
            "Hours_Spent": f"{round(np.clip(np.random.normal(1.5,0.7),0.25,6),2)}",
            "Registered_Flag": "Yes",
            "RSVP_Date": rand_date(2015, 2025),
            "Followup_Sent": random.choice(["Yes","No"]),
            "Followup_Response": random.choice(["Yes","No","Later"]),
            "Badge_Earned": random.choice(["Volunteer","Speaker","Mentor","Attendee"]),
            "Certificate_Issued": random.choice(["Yes","No"]),
            "Photo_Consent": random.choice(["Yes","No"]),
            "Comments": random.choice(["Looking for internship","Great panelists","Would attend again","Good content"]),
            "Created_At": rand_date(2015, 2025),
            "Updated_At": rand_date(2015, 2025)
        })
    df = pd.DataFrame(rows); ensure_no_nulls(df,"engagements")
    assert df["Alumni_ID"].isin(alumni_df["Alumni_ID"]).all()
    assert df["Event_ID"].isin(events_df["Event_ID"]).all()
    df.to_csv("engagements.csv", index=False)

def verify_all():
    req = {
        "employers":"Employer_ID",
        "alumni":"Alumni_ID",
        "students":"Student_ID",
        "events":"Event_ID",
        "jobs":"Job_ID",
        "engagements":"Engagement_ID",
    }
    for f, pk in req.items():
        assert os.path.exists(f"{f}.csv"), f"missing {f}.csv"
        df = pd.read_csv(f"{f}.csv")
        print(f"{f}.csv -> shape={df.shape}, pk_unique={df[pk].is_unique}")
        ensure_no_nulls(df, f)
    # FK checks
    a = pd.read_csv("alumni.csv"); e = pd.read_csv("employers.csv")
    j = pd.read_csv("jobs.csv"); v = pd.read_csv("events.csv")
    g = pd.read_csv("engagements.csv"); s = pd.read_csv("students.csv")
    assert j["Alumni_ID"].isin(a["Alumni_ID"]).all()
    assert j["Employer_ID"].isin(e["Employer_ID"]).all()
    assert g["Alumni_ID"].isin(a["Alumni_ID"]).all()
    assert g["Event_ID"].isin(v["Event_ID"]).all()
    assert s["Current_Employer_ID"].astype(int).isin(e["Employer_ID"]).all()
    print("All integrity checks passed ✅")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Generate one table at a time (1000×20, no nulls).")
    p.add_argument("table", choices=["employers","alumni","students","events","jobs","engagements","verify"])
    args = p.parse_args()
    fn = {
        "employers": make_employers,
        "alumni": make_alumni,
        "students": make_students,
        "events": make_events,
        "jobs": make_jobs,
        "engagements": make_engagements,
        "verify": verify_all,
    }[args.table]
    fn()
    if args.table != "verify":
        print(f"Done -> {args.table}.csv (1000×20, no nulls).")