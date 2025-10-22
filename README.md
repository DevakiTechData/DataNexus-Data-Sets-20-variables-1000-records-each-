# 🎓 DataNexus SLU Alumni Connect – Synthetic Dataset

**Repository:** [DataNexus-Collected-Data](https://github.com/DevakiTechData/DataNexus-Collected-Data)  
**Created by:** Group-2 (Devaki B, Keerthi A, Sri Lasya G, Harsha Priya C, Sanjeev Kumar B)  
**University:** Saint Louis University  
**Course:** IS-5960 – Master Research Project  
**Instructor:** Maria Weber  
**Date:** October 2025  

---

## 📘 Project Overview

The **DataNexus SLU Alumni Connect Platform** is a research capstone project designed to help Saint Louis University (SLU) analyze and strengthen connections between **MS students, alumni, and employers**.  
This dataset supports the analytical dashboards used in the project by providing realistic, ethically generated data that mimics SLU’s academic and employment ecosystem.

---

## 🎯 Objectives

- Track **student progression** from enrollment to employment (CPT → OPT → STEM-OPT → Full-Time).  
- Analyze **alumni outcomes**, technologies, and job trends.  
- Explore **employer partnerships** and engagement patterns.  
- Evaluate **university event participation** and its impact on student-employer relationships.  

---

## 🧩 Dataset Structure

| File Name | Description | Records | Key Fields |
|------------|-------------|----------|-------------|
| **students.csv** | Current MS students with enrollment, visa status, GPA, and internship details | 1,000 | `Student_ID` (PK), `Current_Employer_ID` (FK) |
| **alumni.csv** | Alumni data including graduation year, work phase, employer, and technologies | 1,000 | `Alumni_ID` (PK) |
| **employers.csv** | Employer and partnership information (industry, size, contact, location) | 1,000 | `Employer_ID` (PK) |
| **jobs.csv** | Links alumni to employers with job details, salaries, technologies, and dates | 1,000 | `Job_ID` (PK), `Alumni_ID` (FK), `Employer_ID` (FK) |
| **events.csv** | University and employer events (career fairs, workshops, meetups) | 1,000 | `Event_ID` (PK) |
| **engagements.csv** | Alumni participation in events with feedback and engagement scores | 1,000 | `Engagement_ID` (PK), `Alumni_ID` (FK), `Event_ID` (FK) |
| **data_dictionary.csv** | Metadata describing each column’s name, type, and example | — | — |

**Total Records:** ~6,000  
**Variables per Table:** 20  
**Format:** CSV (comma-separated)  
**Structure:** Relational (normalized)  

---

## 🧠 Data Generation Details

- **Data Source:** Synthetic dataset generated using **Python 3.13**, **Faker**, **NumPy**, and **Pandas**.  
- **Collection Date:** October 2025  
- **Date Range Covered:** 2015 – 2025 (student enrollment, alumni graduation, employment, and events).  
- **Ethics & Privacy:** All data is **fictional**, with no personally identifiable or institutional information.

### Generation Steps
1. Designed an **Entity Relationship Diagram (ERD)** defining six core entities.  
2. Generated 1,000 records per entity using **Faker** for names, emails, and locations.  
3. Created numeric and date fields using **NumPy** and **datetime** ranges.  
4. Ensured **20 columns per table** with **no null or empty values**.  
5. Verified all **primary/foreign key integrity** and unique IDs.  
6. Compiled a **data dictionary** for column metadata.  

Verification output:
