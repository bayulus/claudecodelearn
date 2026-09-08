"""
career-analysis.py

Interactive cybersecurity career path advisor.
Answer a few questions about what you enjoy, get matched to
cybersecurity roles (SOC, DFIR, Pentest, etc.), then pick one
to learn what the job actually involves.
"""

import sys

# ---------------------------------------------------------------------------
# Role definitions: description, day-to-day, skills, and how to get started.
# ---------------------------------------------------------------------------

ROLES = {
    "SOC Analyst": {
        "summary": "Front-line defender who watches alerts and traffic in real time to catch attacks as they happen.",
        "day_to_day": [
            "Monitor SIEM dashboards (Splunk, Sentinel, QRadar) for suspicious alerts",
            "Triage alerts to separate false positives from real incidents",
            "Escalate confirmed incidents to Tier 2/3 or the DFIR team",
            "Write shift notes and basic incident tickets",
        ],
        "skills": ["Networking fundamentals (TCP/IP, DNS, HTTP)", "Log analysis", "SIEM tools", "Basic scripting (Python/PowerShell)"],
        "getting_started": "Entry-level friendly. Certs like Security+, CySA+, or a SOC analyst bootcamp/home-lab (Blue Team Labs, LetsDefend) are common starting points.",
    },
    "DFIR (Digital Forensics & Incident Response)": {
        "summary": "The investigator who steps in after something bad happens: figures out what occurred, how far it spread, and how to clean it up.",
        "day_to_day": [
            "Analyze compromised systems, memory dumps, and disk images",
            "Reconstruct attacker timelines from logs and artifacts",
            "Contain and eradicate active threats during an incident",
            "Write formal incident reports for leadership/legal/clients",
        ],
        "skills": ["Malware/forensic analysis tools (Volatility, Autopsy, EnCase)", "Deep OS internals (Windows/Linux)", "Log correlation", "Calm, methodical thinking under pressure"],
        "getting_started": "Usually a step up from SOC or sysadmin work. Certs: GCFA, GCIH, GNFA. Practice with forensic CTFs (CyberDefenders, DFIR.Training).",
    },
    "Penetration Tester / Red Teamer": {
        "summary": "The ethical attacker: gets paid to break into systems before real criminals do, then reports how.",
        "day_to_day": [
            "Scope and run authorized attacks against networks, apps, or physical sites",
            "Exploit vulnerabilities to demonstrate real business impact",
            "Write detailed reports with reproduction steps and fixes",
            "Stay current on new exploits, tools, and techniques",
        ],
        "skills": ["Offensive tools (Metasploit, Burp Suite, Cobalt Strike)", "Scripting/exploit dev", "Web/network/AD attack techniques", "Clear technical writing"],
        "getting_started": "Certs: PJPT, OSCP, eJPT. Practice on HackTheBox, TryHackMe, and CTFs. A bug bounty track record also opens doors.",
    },
    "Threat Intelligence Analyst": {
        "summary": "The researcher who studies attackers themselves — who they are, what they want, and what they'll likely do next.",
        "day_to_day": [
            "Track threat actor groups, malware families, and campaigns",
            "Turn raw intel (IOCs, TTPs) into reports decision-makers can act on",
            "Brief SOC/DFIR teams on emerging threats relevant to the org",
            "Use frameworks like MITRE ATT&CK to map adversary behavior",
        ],
        "skills": ["OSINT research", "Malware behavior analysis", "Structured writing/briefing", "Frameworks: MITRE ATT&CK, Diamond Model"],
        "getting_started": "Certs: GCTI. Strong writing skills matter as much as technical ones. Start by following threat research blogs and writing your own IOC reports.",
    },
    "Security Engineer": {
        "summary": "The builder who designs and hardens the systems and defenses everyone else relies on.",
        "day_to_day": [
            "Design and deploy security tooling (firewalls, EDR, IAM, SIEM pipelines)",
            "Automate detection and response with code",
            "Harden infrastructure and review architecture for security gaps",
            "Partner with IT/dev teams to bake security into new systems",
        ],
        "skills": ["Strong scripting/automation (Python, Terraform)", "Cloud platforms (AWS/Azure/GCP)", "Systems/network administration", "Security architecture"],
        "getting_started": "Often a path from sysadmin/DevOps or SOC. Certs: Security+, AWS/Azure security certs, GSEC.",
    },
    "Application Security (AppSec) Engineer": {
        "summary": "The specialist who makes sure software itself isn't the weak link — finding and fixing flaws in code before attackers do.",
        "day_to_day": [
            "Perform code reviews and static/dynamic analysis (SAST/DAST)",
            "Threat-model new features during design",
            "Work with developers to fix vulnerabilities (SQLi, XSS, auth flaws)",
            "Build secure coding guidelines and CI/CD security gates",
        ],
        "skills": ["Programming (JavaScript, Python, Java, etc.)", "OWASP Top 10", "Static/dynamic analysis tools", "Collaboration with dev teams"],
        "getting_started": "Great fit for developers moving into security. Certs: eWPT, OSWE. Practice on OWASP Juice Shop and PortSwigger Web Security Academy.",
    },
    "GRC (Governance, Risk & Compliance) Analyst": {
        "summary": "The strategist who makes sure the organization meets security standards, manages risk, and stays out of legal trouble.",
        "day_to_day": [
            "Assess compliance against frameworks (ISO 27001, NIST, SOC 2, PCI-DSS)",
            "Run risk assessments and track remediation plans",
            "Write and maintain security policies",
            "Coordinate audits with internal/external stakeholders",
        ],
        "skills": ["Knowledge of compliance frameworks", "Risk assessment methods", "Policy writing", "Communication with non-technical stakeholders"],
        "getting_started": "Good fit for detail-oriented, people-facing thinkers. Certs: CISA, CRISC, ISO 27001 Lead Auditor.",
    },
    "Cloud Security Engineer": {
        "summary": "The specialist who secures apps and data running in AWS/Azure/GCP instead of traditional on-prem networks.",
        "day_to_day": [
            "Audit cloud configurations for misconfigurations (open S3 buckets, over-permissive IAM)",
            "Implement cloud-native security tools (CSPM, CWPP)",
            "Secure CI/CD pipelines and infrastructure-as-code",
            "Respond to cloud-specific incidents",
        ],
        "skills": ["Deep knowledge of one or more cloud platforms", "IAM design", "Infrastructure as code (Terraform)", "Container/Kubernetes security"],
        "getting_started": "Certs: AWS Certified Security - Specialty, Azure Security Engineer. Best approached after general cloud or security fundamentals.",
    },
}

# ---------------------------------------------------------------------------
# Questions: each option maps to a dict of {role: points}
# ---------------------------------------------------------------------------

QUESTIONS = [
    {
        "text": "What sounds most satisfying to you?",
        "options": [
            ("Catching something bad happening right now", {"SOC Analyst": 3, "DFIR (Digital Forensics & Incident Response)": 1}),
            ("Digging into what already happened and piecing the story together", {"DFIR (Digital Forensics & Incident Response)": 3, "Threat Intelligence Analyst": 1}),
            ("Breaking into a system before the bad guys do", {"Penetration Tester / Red Teamer": 3}),
            ("Studying attackers and predicting their next move", {"Threat Intelligence Analyst": 3}),
            ("Building tools and systems that prevent problems in the first place", {"Security Engineer": 3, "Cloud Security Engineer": 1}),
            ("Reviewing code and fixing security bugs in software", {"Application Security (AppSec) Engineer": 3}),
            ("Making sure the organization follows the rules and manages risk", {"GRC (Governance, Risk & Compliance) Analyst": 3}),
        ],
    },
    {
        "text": "Which work style fits you best?",
        "options": [
            ("Fast-paced, real-time monitoring and quick decisions", {"SOC Analyst": 3}),
            ("Slow, methodical investigation with attention to detail", {"DFIR (Digital Forensics & Incident Response)": 3, "GRC (Governance, Risk & Compliance) Analyst": 1}),
            ("Creative problem solving, thinking like an adversary", {"Penetration Tester / Red Teamer": 3}),
            ("Research and writing reports/briefings", {"Threat Intelligence Analyst": 3}),
            ("Hands-on building/automating infrastructure", {"Security Engineer": 3, "Cloud Security Engineer": 2}),
            ("Reading and writing code", {"Application Security (AppSec) Engineer": 3}),
            ("Talking with people, policies, and audits", {"GRC (Governance, Risk & Compliance) Analyst": 3}),
        ],
    },
    {
        "text": "Which of these have you already enjoyed doing (even informally)?",
        "options": [
            ("Watching logs/dashboards or setting up home lab alerts", {"SOC Analyst": 3}),
            ("Recovering deleted files or analyzing a weird system issue", {"DFIR (Digital Forensics & Incident Response)": 3}),
            ("CTFs, HackTheBox, or trying to bypass restrictions", {"Penetration Tester / Red Teamer": 3}),
            ("Reading about hacker groups, malware, or breach reports", {"Threat Intelligence Analyst": 3}),
            ("Writing scripts to automate a repetitive task", {"Security Engineer": 2, "Cloud Security Engineer": 2, "Application Security (AppSec) Engineer": 1}),
            ("Building or debugging an app/website", {"Application Security (AppSec) Engineer": 3}),
            ("Organizing documents, processes, or checklists", {"GRC (Governance, Risk & Compliance) Analyst": 3}),
            ("Working with AWS/Azure/GCP", {"Cloud Security Engineer": 3}),
        ],
    },
    {
        "text": "Which statement describes your ideal impact?",
        "options": [
            ("I stop the attack while it's happening", {"SOC Analyst": 3}),
            ("I find the full truth after an incident and help recover", {"DFIR (Digital Forensics & Incident Response)": 3}),
            ("I find the hole before someone else exploits it", {"Penetration Tester / Red Teamer": 3, "Application Security (AppSec) Engineer": 1}),
            ("I help others understand the threat landscape", {"Threat Intelligence Analyst": 3}),
            ("I make systems resilient by design", {"Security Engineer": 3, "Cloud Security Engineer": 2}),
            ("I make sure the organization is compliant and low-risk", {"GRC (Governance, Risk & Compliance) Analyst": 3}),
        ],
    },
]


def ask_question(question):
    """Print a question with numbered options and return the chosen option's scores."""
    print(f"\n{question['text']}")
    for i, (label, _) in enumerate(question["options"], start=1):
        print(f"  {i}. {label}")

    while True:
        choice = input("Your choice: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(question["options"]):
            return question["options"][int(choice) - 1][1]
        print(f"Please enter a number between 1 and {len(question['options'])}.")


def run_quiz():
    scores = {role: 0 for role in ROLES}
    for question in QUESTIONS:
        result = ask_question(question)
        for role, points in result.items():
            scores[role] += points
    return scores


def show_results(scores):
    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    print("\n" + "=" * 60)
    print("YOUR CYBERSECURITY CAREER MATCHES")
    print("=" * 60)
    for rank, (role, points) in enumerate(ranked[:5], start=1):
        print(f"  {rank}. {role}  (score: {points})")
    print("=" * 60)
    return ranked


def explain_role(role):
    info = ROLES[role]
    print("\n" + "-" * 60)
    print(role.upper())
    print("-" * 60)
    print(f"\n{info['summary']}\n")
    print("What you'd actually do day-to-day:")
    for item in info["day_to_day"]:
        print(f"  - {item}")
    print("\nSkills that matter most:")
    for item in info["skills"]:
        print(f"  - {item}")
    print(f"\nHow to get started:\n  {info['getting_started']}")
    print("-" * 60)


def role_menu(ranked):
    role_names = [role for role, _ in ranked]
    while True:
        print("\nWant to learn more about a role?")
        for i, role in enumerate(role_names, start=1):
            print(f"  {i}. {role}")
        print("  0. Exit")

        choice = input("Your choice: ").strip()
        if choice == "0":
            print("\nGood luck on your cybersecurity journey!")
            return
        if choice.isdigit() and 1 <= int(choice) <= len(role_names):
            explain_role(role_names[int(choice) - 1])
        else:
            print("Please enter a valid number.")


def main():
    print("=" * 60)
    print("CYBERSECURITY CAREER PATH ADVISOR")
    print("=" * 60)
    print("Answer a few quick questions about what you enjoy,")
    print("and we'll point you toward matching cybersecurity roles.")

    try:
        scores = run_quiz()
        ranked = show_results(scores)
        role_menu(ranked)
    except (KeyboardInterrupt, EOFError):
        print("\n\nExiting. See you next time!")
        sys.exit(0)


if __name__ == "__main__":
    main()
