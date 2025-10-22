# 🎓 DataNexus SLU Alumni Connect – Synthetic Dataset & Python Generation Scripts

**Repository:** [DataNexus-Collected-Data](https://github.com/DevakiTechData/DataNexus-Collected-Data)  
**Created by:** Group-2 – Devaki B, Keerthi A, Sri Lasya G, Harsha Priya C, Sanjeev Kumar B  
**University:** Saint Louis University  
**Course:** IS-5960 – Master Research Project  
**Instructor:** Maria Weber  
**Date:** October 2025  

---

## 🧭 Project Overview

The **DataNexus SLU Alumni Connect Platform** is a capstone research project that enables Saint Louis University (SLU)  
to analyze and strengthen engagement between **MS students, alumni, and employers**.  
It supports decision-making through dashboards that show trends in:
- student academic progress and visa phases (CPT → OPT → STEM-OPT → Full-Time)
- alumni career outcomes, roles, and technologies
- employer hiring patterns and partnership levels
- university and employer event participation

To build and test these dashboards safely, the team created a **synthetic dataset** that mirrors real-world structure but  
contains **no personally identifiable information (PII)**.

---

## 🎯 Capstone Objectives

- Map SLU MS students’ journey from enrollment to employment.  
- Identify the top employers and technologies for SLU graduates.  
- Analyze event participation to improve academic-industry collaboration.  
- Provide a secure, ethical data foundation for data governance and visualization.

---

## 🧩 Dataset Composition

| File Name | Description | Records | Key Fields |
|------------|-------------|----------|-------------|
| **students.csv** | Active SLU MS students with demographics, GPA, and internship details. | 1,000 | `Student_ID` (PK), `Current_Employer_ID` (FK) |
| **alumni.csv** | Alumni career data, including graduation year, work phase, and job details. | 1,000 | `Alumni_ID` (PK) |
| **employers.csv** | Employer profiles, contact information, and partnership attributes. | 1,000 | `Employer_ID` (PK) |
| **jobs.csv** | Links alumni to employers, including salary, role, technology, and dates. | 1,000 | `Job_ID` (PK), `Alumni_ID` (FK), `Employer_ID` (FK) |
| **events.csv** | University and employer events with type, duration, and feedback. | 1,000 | `Event_ID` (PK) |
| **engagements.csv** | Alumni participation records, feedback, and engagement ratings. | 1,000 | `Engagement_ID` (PK), `Alumni_ID` (FK), `Event_ID` (FK) |
| **data_dictionary.csv** | Variable names, data types, and sample values for all tables. | — | — |

**Total Records:** ~6,000  
**Columns per Table:** 20  
**Format:** CSV (comma-separated)  
**Structure:** Normalized relational schema aligned to the project ERD  

---

## 🧠 Data Generation Process

### Tools Used
- **Python 3.13**
- **Libraries:** `Faker`, `NumPy`, `Pandas`
- **IDE:** Visual Studio Code / Terminal on macOS

### Generation Scripts
| Script | Purpose |
|---------|----------|
| `make_table.py` | Modular generator — creates each table (students, alumni, employers, jobs, events, engagements) individually, ensuring 1000×20 format, no nulls, and valid foreign keys. |
| `generate_1000x20_nonnull.py` | Combined script that builds all six tables at once (optional). |

---

### How Data Was Created
1. Designed an **Entity Relationship Diagram (ERD)** showing relationships among all six tables.  
2. Used **Faker** to generate names, emails, cities, companies, and job titles.  
3. Used **NumPy** for numeric realism (salaries, participation scores, GPAs, etc.).  
4. Generated consistent date ranges (2015 – 2025) for enrollment, graduation, and events.  
5. Enforced:
   - 1000 records per table  
   - 20 columns per table  
   - no nulls or empty values  
   - valid PK/FK links across all entities  
6. Exported verified tables as `.csv` and metadata as `data_dictionary.csv`.  
7. Committed all files to GitHub for reproducibility.

---

## ✅ Verification Output

Example console validation:

python ~/make_table.py verify

employers.csv -> shape=(1000, 20), pk_unique=True
alumni.csv -> shape=(1000, 20), pk_unique=True
students.csv -> shape=(1000, 20), pk_unique=True
events.csv -> shape=(1000, 20), pk_unique=True
jobs.csv -> shape=(1000, 20), pk_unique=True
engagements.csv -> shape=(1000, 20), pk_unique=True
All integrity checks passed ✅



This confirms:
- Correct record counts and column counts  
- Primary key uniqueness  
- Foreign-key integrity  
- No missing or blank fields  

---

## 📂 Directory Structure
DataNexus-Collected-Data/
│
├── README.md
├── make_table.py
├── generate_1000x20_nonnull.py
│
├── students.csv
├── alumni.csv
├── employers.csv
├── jobs.csv
├── events.csv
├── engagements.csv
├── data_dictionary.csv
│
└── Entity Relationship Diagram FINAL.pdf


---

## ⚙️ How to Regenerate the Data

### 1️⃣ Activate virtual environment
```bash
source ~/venv/bin/activate

2️⃣ Install dependencies
pip install faker pandas numpy

3️⃣ Generate each table
python make_table.py employers
python make_table.py alumni
python make_table.py students
python make_table.py events
python make_table.py jobs
python make_table.py engagements

4️⃣ Verify results
python make_table.py verify

5️⃣ Rebuild data dictionary (optional)
python - << 'PY'
import pandas as pd, glob
rows=[]
for f in glob.glob("*.csv"):
    if f!="data_dictionary.csv":
        df=pd.read_csv(f)
        for c in df.columns:
            rows.append({"Table":f.replace(".csv",""),"Column":c,"Dtype":str(df[c].dtype),"Example":str(df[c].iloc[0])})
pd.DataFrame(rows).to_csv("data_dictionary.csv",index=False)
print("data_dictionary.csv rebuilt ✅")
PY

💻 How to Explore the Dataset
Python (Pandas)
import pandas as pd
df = pd.read_csv("students.csv")
print(df.shape)
print(df.head())

Power BI / Tableau / Excel

Import all .csv files.

Define relationships based on foreign keys (Employer_ID, Alumni_ID, Event_ID).

Build dashboards to analyze:

Student–Employer engagement

Alumni outcomes by year

Event participation and feedback

🧮 Data Quality & Limitations
Aspect	Description
Authenticity	100% synthetic — generated via Faker; no real PII.
Completeness	Each table has exactly 1000×20 values, no nulls or blanks.
Integrity	All primary and foreign keys validated through script.
Randomness	Controlled random seeds (reproducible results).
Limitation	Data reflects structure and scale, not real-world accuracy.
Use Case	Educational, analytical, and testing purposes only.
📊 Intended Uses

Academic analytics & dashboard demonstrations

Data governance and ETL pipeline design

Machine learning / AI testing with synthetic tabular data

Secure demonstrations of data privacy & ethics in practice

⚠️ Disclaimer:
This dataset is entirely synthetic and for educational use only.
It does not represent real individuals, organizations, or SLU records.

🔐 Ethics & Compliance

Complies with SLU’s Acceptable Use Policy (AUP).

Aligns with NIST AI RMF and Data Ethics Framework for synthetic data.

No sensitive, confidential, or personal data was used or stored.

Random seed ensures reproducible but anonymous output.

🧾 References

Faker Documentation

Pandas Documentation

NumPy Documentation

Saint Louis University – Master Research Project (IS-5960)

📦 Version History
Version	Date	Description
v1.0	Oct 2025	Initial dataset (1000×20 tables, all verified)
v1.1	Oct 2025	Added Python generation scripts & documentation
v1.2	Oct 2025	Final README and data dictionary rebuild
