"""
Script to create seed FAQs for the Campus Assistant chatbot.
Run this script to generate seed_faqs.json file.
"""
import json

faqs = [
    {
        "question": "What are the admission requirements for B.Tech?",
        "answer": "For admission to B.Tech programs, candidates must have passed 12th with Physics, Chemistry, and Mathematics with minimum 45% marks (40% for reserved categories). Admission is through JEE Main counseling or state-level counseling conducted by RTU. Documents required: 10th marksheet, 12th marksheet, JEE Main scorecard, domicile certificate, caste certificate (if applicable), and passport-size photographs.",
        "category": "admission",
        "language": "en",
        "keywords": ["admission", "requirements", "eligibility", "btech", "jee", "12th", "marks"],
        "priority": 10
    },
    {
        "question": "What is the fee structure for engineering courses?",
        "answer": "Annual tuition fee for B.Tech is Rs. 65,000 for general category and Rs. 32,500 for reserved categories (SC/ST/OBC). Additional fees: Development fee Rs. 5,000, Exam fee Rs. 2,500/semester, Library Rs. 1,000, Lab Rs. 3,000. Hostel Rs. 35,000/year including mess. Total first year: Rs. 1,10,000 (day scholar), Rs. 1,45,000 (hosteler).",
        "category": "fees",
        "language": "en",
        "keywords": ["fee", "fees", "tuition", "hostel", "cost", "payment", "structure"],
        "priority": 10
    },
    {
        "question": "What scholarships are available for students?",
        "answer": "Scholarships available: 1) Mukhyamantri Ucch Shiksha Scholarship (Rs. 5,000/year for >60% in 12th), 2) Post Matric Scholarship for SC/ST/OBC, 3) Merit-based scholarship for top 10% (50% fee waiver), 4) Pragati Scholarship for girls (Rs. 30,000/year), 5) Central Sector Scholarship. Apply at scholarships.gov.in before deadline.",
        "category": "scholarship",
        "language": "en",
        "keywords": ["scholarship", "financial aid", "fee waiver", "merit", "sc", "st", "obc"],
        "priority": 9
    },
    {
        "question": "How to apply for hostel accommodation?",
        "answer": "Hostel application: 1) Fill form from hostel office/website, 2) Submit with admission receipt and ID, 3) Pay Rs. 35,000 (includes mess), 4) Get room allotment from warden. Facilities: 24/7 security, WiFi, mess, common room. Priority for outstation students. Apply within 15 days of admission.",
        "category": "hostel",
        "language": "en",
        "keywords": ["hostel", "accommodation", "room", "mess", "warden", "stay", "boarding"],
        "priority": 8
    },
    {
        "question": "What is the examination pattern?",
        "answer": "Each semester: 1) Mid-term exam (20% weightage) after 8 weeks, 2) End-term exam (60% weightage), 3) Internal assessment (20%) - assignments, quizzes, attendance. Passing: 40% theory, 50% practical. 75% attendance required. Supplementary exams within 2 months for failed subjects. Results on RTU website.",
        "category": "examination",
        "language": "en",
        "keywords": ["exam", "examination", "marks", "passing", "result", "semester", "attendance"],
        "priority": 8
    },
    {
        "question": "What are the placement opportunities?",
        "answer": "Placement Cell organizes campus recruitment Aug-March. Top recruiters: TCS, Infosys, Wipro, L&T, HCL, Capgemini, and core companies. Average package Rs. 4-6 LPA, highest Rs. 12 LPA. Pre-placement training from 5th semester includes aptitude, communication, technical skills. Eligibility: 60% aggregate, no active backlogs.",
        "category": "placement",
        "language": "en",
        "keywords": ["placement", "job", "campus", "recruitment", "package", "salary", "company", "career"],
        "priority": 9
    },
    {
        "question": "How to get bonafide certificate and other documents?",
        "answer": "From Administrative Office (Room 101): 1) Bonafide: Form + Rs. 50, ready in 2 days, 2) Character Certificate: Form + Rs. 50, 3 days, 3) Migration: Form + Rs. 200 + marksheets, 7 days, 4) Duplicate ID: FIR copy + Rs. 200, 5 days. Office hours: 10 AM - 5 PM, Mon-Sat.",
        "category": "documents",
        "language": "en",
        "keywords": ["certificate", "bonafide", "character", "migration", "document", "id card"],
        "priority": 8
    },
    {
        "question": "What are the contact details for departments?",
        "answer": "Key contacts: Principal: 0141-2345678, Admission: 0141-2345679, Exam Cell: 0141-2345680, Boys Hostel: 0141-2345681, Girls Hostel: 0141-2345682, Placement: 0141-2345683, Library: 0141-2345684. Emergency: 0141-2345600 (24/7). Email: info@college.edu",
        "category": "contact",
        "language": "en",
        "keywords": ["contact", "phone", "email", "office", "department", "helpline"],
        "priority": 7
    },
    {
        "question": "What are the anti-ragging rules?",
        "answer": "Ragging is criminal offense with severe consequences: suspension, expulsion, FIR under IPC, fine up to Rs. 25,000. Report ragging: 1) Helpline: 1800-180-5522, 2) Email: helpline@antiragging.in, 3) College Anti-Ragging Committee, 4) Local police. All freshers must submit affidavit at antiragging.in.",
        "category": "grievance",
        "language": "en",
        "keywords": ["ragging", "harassment", "complaint", "helpline", "punishment", "senior"],
        "priority": 10
    },
    {
        "question": "What are the college timings?",
        "answer": "College timings: Morning 9 AM-1 PM, Lunch 1-2 PM, Afternoon 2-5 PM. Labs may extend till 6 PM. Admin office: 10 AM-5 PM (Mon-Sat). Library: 9 AM-8 PM. Hostel gates: 9 PM (10 PM during exams). Closed Sundays and government holidays.",
        "category": "general",
        "language": "en",
        "keywords": ["timing", "hours", "schedule", "open", "close", "working", "office"],
        "priority": 7
    },
    {
        "question": "B.Tech mein admission ke liye kya eligibility hai?",
        "answer": "B.Tech ke liye 12th class Physics, Chemistry, Mathematics ke saath 45% marks chahiye (reserved category 40%). Admission JEE Main counseling ya Rajasthan state counseling se hota hai. Documents: 10th marksheet, 12th marksheet, JEE score, domicile certificate, caste certificate. RTU website par counseling dates dekhen.",
        "category": "admission",
        "language": "hi",
        "keywords": ["admission", "eligibility", "btech", "jee", "12th", "pravesh"],
        "priority": 10
    },
    {
        "question": "Fees kitni hai engineering course ki?",
        "answer": "B.Tech annual fees: General category Rs. 65,000, Reserved (SC/ST/OBC) Rs. 32,500. Development fee Rs. 5,000, Exam fee Rs. 2,500/semester. Hostel Rs. 35,000/year with mess. Day scholar total Rs. 1,10,000, Hosteler Rs. 1,45,000 first year mein.",
        "category": "fees",
        "language": "hi",
        "keywords": ["fees", "shulk", "paisa", "hostel", "tuition", "cost"],
        "priority": 10
    },
    {
        "question": "Scholarship kaise milti hai?",
        "answer": "Scholarships: 1) Mukhyamantri Ucch Shiksha Scholarship Rs. 5,000/saal (12th mein 60%+), 2) Post Matric Scholarship SC/ST/OBC ke liye, 3) Merit scholarship top 10% ko 50% fee maaf, 4) Pragati Scholarship ladkiyon ke liye Rs. 30,000/saal. Apply: scholarships.gov.in par register karein.",
        "category": "scholarship",
        "language": "hi",
        "keywords": ["scholarship", "chatravritti", "paisa", "help", "merit", "sc", "st"],
        "priority": 9
    },
    {
        "question": "Placement kaise hoti hai?",
        "answer": "Placement Cell August se March tak campus recruitment organize karti hai. Top companies: TCS, Infosys, Wipro, L&T, HCL, Capgemini. Average package Rs. 4-6 LPA, highest Rs. 12 LPA. Training 5th semester se shuru. Eligibility: 60% aggregate, koi backlog nahi hona chahiye.",
        "category": "placement",
        "language": "hi",
        "keywords": ["placement", "naukri", "job", "company", "salary", "package", "campus"],
        "priority": 9
    },
    {
        "question": "Hostel mein room kaise milega?",
        "answer": "Hostel ke liye: 1) Form hostel office ya website se lein, 2) Admission receipt aur ID ke saath submit karein, 3) Rs. 35,000 fee jama karein (mess included), 4) Warden se room allotment lein. WiFi, mess, 24/7 security available hai. Outstation students ko priority milti hai.",
        "category": "hostel",
        "language": "hi",
        "keywords": ["hostel", "room", "rehna", "mess", "accommodation", "stay"],
        "priority": 8
    },
    {
        "question": "How to apply for education loan?",
        "answer": "Education loan process: 1) Get admission confirmation letter, 2) Fee structure from college, 3) Apply at SBI/PNB/BOB, 4) Documents: marksheets, admission letter, parents income proof, ID proofs, 5) Loan up to Rs. 10 lakhs without collateral, 6) Interest 8.5-10%. Check vidyalakshmi.co.in for comparison.",
        "category": "fees",
        "language": "en",
        "keywords": ["loan", "education", "bank", "finance", "emi", "interest", "vidyalakshmi"],
        "priority": 8
    },
    {
        "question": "What happens if I fail in a subject?",
        "answer": "If you fail: 1) Appear in supplementary exam within 2 months, 2) Fee Rs. 500/subject, 3) Maximum 4 attempts allowed, 4) Failed subjects don't block next semester (lateral carry), 5) Clear all backlogs before degree, 6) More than 3 active backlogs may affect placement eligibility.",
        "category": "examination",
        "language": "en",
        "keywords": ["fail", "backlog", "supplementary", "reexam", "atkt", "compartment"],
        "priority": 8
    },
    {
        "question": "How to get internship opportunities?",
        "answer": "Internships: 1) Summer internships (May-July) coordinated by Placement Cell, 2) Register on placement portal, 3) TCS, Infosys offer programs, 4) Stipend Rs. 10,000-25,000/month, 5) Mandatory 4-week training in 6th semester, 6) Check internship.aicte-india.org. Faculty can recommend IIT/NIT research internships.",
        "category": "placement",
        "language": "en",
        "keywords": ["internship", "training", "summer", "industry", "stipend", "experience"],
        "priority": 7
    },
    {
        "question": "What B.Tech branches are available?",
        "answer": "B.Tech specializations: 1) Computer Science (CSE) - 120 seats, 2) Information Technology (IT) - 60 seats, 3) Electronics & Communication (ECE) - 60 seats, 4) Electrical Engineering - 60 seats, 5) Mechanical Engineering - 120 seats, 6) Civil Engineering - 60 seats, 7) CSE (AI/ML) - 60 seats. All AICTE approved, RTU affiliated.",
        "category": "admission",
        "language": "en",
        "keywords": ["branch", "specialization", "cse", "it", "ece", "mechanical", "civil", "seats"],
        "priority": 8
    },
    {
        "question": "How to access library resources?",
        "answer": "Library open 9 AM-8 PM on working days. Get library card with college ID. Borrow up to 4 books for 14 days. Late fine Rs. 2/day. Digital resources: NPTEL videos, e-journals via DELNET, previous year papers. E-books accessible with student login credentials.",
        "category": "library",
        "language": "en",
        "keywords": ["library", "books", "borrow", "card", "journals", "ebooks", "nptel"],
        "priority": 7
    },
    {
        "question": "How to report a grievance or complaint?",
        "answer": "For grievances: 1) Academic issues: Contact HOD or Dean, 2) Hostel issues: Warden or Chief Warden, 3) Ragging: Anti-Ragging Cell (1800-180-5522), 4) Sexual harassment: Internal Complaints Committee (ICC), 5) General: Principal's grievance cell. Complaints addressed within 7 working days.",
        "category": "grievance",
        "language": "en",
        "keywords": ["complaint", "grievance", "ragging", "harassment", "issue", "problem", "report"],
        "priority": 8
    },
    {
        "question": "What is the process for branch change?",
        "answer": "Branch change after 1st year based on merit. Eligibility: 1) Clear all 1st year subjects first attempt, 2) No disciplinary action, 3) Minimum 8.0 CGPA. Process: Apply online June-July, merit list by CGPA, allotment based on seats. Up to 10% of branch intake available. CSE/IT have high competition.",
        "category": "admission",
        "language": "en",
        "keywords": ["branch", "change", "transfer", "cgpa", "cse", "switch"],
        "priority": 6
    },
    {
        "question": "Is there bus facility for students?",
        "answer": "College provides bus on multiple routes covering Jaipur city and nearby areas. Fee Rs. 15,000/semester (distance-based). Routes: Mansarovar, Vaishali Nagar, Malviya Nagar, Sanganer, Sitapura, Tonk Road, Sikar Road. Morning pickup 7:30-8:30 AM, Evening 5 PM. Apply at Transport Office.",
        "category": "transport",
        "language": "en",
        "keywords": ["bus", "transport", "travel", "route", "pickup", "drop"],
        "priority": 6
    },
    {
        "question": "Medical facility kaisi hai college mein?",
        "answer": "College mein medical room hai jahan First Aid milta hai (10 AM-5 PM). Doctor weekly 2 din aate hain (Tuesday, Thursday). Emergency: College ambulance available. Nearby SMS Hospital 5 km. Group medical insurance Rs. 1 lakh cover sabhi students ke liye. Medical leave ke liye doctor certificate chahiye.",
        "category": "general",
        "language": "hi",
        "keywords": ["medical", "doctor", "hospital", "davai", "health", "emergency"],
        "priority": 7
    },
    {
        "question": "Wi-Fi aur computer lab kaise access karein?",
        "answer": "Campus mein free Wi-Fi hai. Credentials Library ya IT department se lein with college ID. Speed 10 Mbps/user. Social media restricted academic hours mein. Computer Lab (Room 201): 9 AM-6 PM. Department labs for practicals. 24/7 access during exams on request. Gaming/torrents prohibited.",
        "category": "facilities",
        "language": "hi",
        "keywords": ["wifi", "internet", "computer", "lab", "laptop", "network"],
        "priority": 6
    },
    {
        "question": "What extracurricular activities are available?",
        "answer": "Clubs: 1) Technical - Robotics, Coding, IEEE, SAE, 2) Cultural - Music, Dance, Drama, 3) Sports - Cricket, Football, Basketball, Volleyball, Chess. NSS and NCC units available. Annual tech fest 'TechnoVision' in February, cultural fest 'Utsav' in March. Join during fresher's week. Sports ground, indoor stadium, gym available.",
        "category": "activities",
        "language": "en",
        "keywords": ["clubs", "sports", "cultural", "technical", "fest", "nss", "ncc", "activities"],
        "priority": 6
    },
    {
        "question": "How to get duplicate marksheet?",
        "answer": "For duplicate marksheet: 1) File FIR at police station, 2) Publish newspaper ad about loss, 3) Apply to RTU with: form, FIR copy, newspaper cutting, 2 photos, Rs. 500 fee, 4) Submit at Exam Cell or RTU directly, 5) Processing 30-45 days. Semester marksheet from college, degree from RTU.",
        "category": "documents",
        "language": "en",
        "keywords": ["marksheet", "duplicate", "lost", "certificate", "degree", "rtu"],
        "priority": 7
    },
    {
        "question": "Fee refund kaise milti hai?",
        "answer": "Fee refund policy: Classes shuru hone se pehle 90%, 15 din mein 80%, 30 din mein 60%, uske baad no refund. Process: 1) Accounts Office mein application + original receipt, 2) Cancellation proof attach karein, 3) Bank details dein, 4) 15-20 working days mein NEFT. Caution money clearance ke baad.",
        "category": "fees",
        "language": "hi",
        "keywords": ["refund", "fee", "cancel", "withdraw", "paisa wapas"],
        "priority": 6
    },
    {
        "question": "What diploma courses are offered?",
        "answer": "3-year diploma courses: 1) Computer Science, 2) Electrical Engineering, 3) Mechanical Engineering, 4) Civil Engineering, 5) Electronics, 6) Automobile Engineering. Eligibility: 10th pass with 35% marks. Admission via DTE Rajasthan counseling or JEN exam. Lateral entry to B.Tech 2nd year through LEET.",
        "category": "admission",
        "language": "en",
        "keywords": ["diploma", "polytechnic", "course", "10th", "lateral", "leet"],
        "priority": 8
    }
]

if __name__ == "__main__":
    with open("seed_faqs.json", "w", encoding="utf-8") as f:
        json.dump(faqs, f, indent=2, ensure_ascii=False)

    print(f"Created seed_faqs.json with {len(faqs)} FAQs")
    print("\nCategories covered:")
    categories = {}
    for faq in faqs:
        cat = faq["category"]
        categories[cat] = categories.get(cat, 0) + 1
    for cat, count in sorted(categories.items()):
        print(f"  - {cat}: {count} FAQs")

    print("\nLanguages:")
    langs = {}
    for faq in faqs:
        lang = faq["language"]
        langs[lang] = langs.get(lang, 0) + 1
    for lang, count in sorted(langs.items()):
        print(f"  - {lang}: {count} FAQs")
