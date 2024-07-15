import re

pattern = r"\b(ABOUT|Overview|OVERVIEW|Summary|SUMMARY|Education|EDUCATION|Experience|EXPERIENCE|Training|TRAINING|TRAININGS|INTERNSHIPS|Projects|PROJECTS|SKILLS|Achievements|ACHIEVEMENTS|$)\b(?!.*\d\+\syears\sof\sexperience)"

# Test string
resume_text = "Summary 3+ years of experience in software development. EXPERIENCE"

# Example of section_start
section_start = 0

# Using the regex to search in the text
match = re.search(pattern, resume_text[section_start+1:])

if match:
    print("Match found:", match.group())
else:
    print("No match found")