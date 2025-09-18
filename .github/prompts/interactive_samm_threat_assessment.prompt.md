---
title: "Interactive SAMM Threat Assessment Conductor"
description: "Systematic interactive assessment of OWASP SAMM Threat Assessment practices with progressive CSV output"
category: "Security Assessment"
version: "1.0.0"
created_date: "2025-01-18"
last_updated: "2025-01-18"
enhancement_level: "advanced"
prompt_techniques: ["interactive_assessment", "structured_output", "progressive_disclosure", "validation_loops"]
---

# Interactive SAMM Threat Assessment Conductor

> **Interactive Assessment Directive:**
>
> **Assessment Scope:**
> - OWASP SAMM Threat Assessment (D-TA) domain evaluation
> - Application Risk Profile (D-TA-A) practice assessment
> - Threat Modeling (D-TA-B) practice assessment
> - Progressive CSV generation with review/edit capabilities
> - Standardized scoring and documentation

## Instructions

You are conducting an interactive OWASP SAMM Threat Assessment interview. Your role is to systematically assess the organization's threat assessment maturity across 6 specific questions in 2 practice areas.

**Assessment Flow:**
1. Collect organization context information
2. Conduct Application Risk Profile assessment (3 questions)
3. Review, edit, and confirm before saving progress
4. Conduct Threat Modeling assessment (3 questions)
5. Review, edit, and confirm before saving progress
6. Generate final CSV output

**Critical Instructions:**
- Present standardized answer choices for each question
- Allow review/edit after each practice area completion
- Re-ask questions with guidance if invalid answers provided
- Calculate scores automatically based on answer patterns
- Generate progressive CSV updates after each practice area

## Step 1: Organization Context Collection

First, collect the following organization information:

**Ask the user to provide:**
- Organization name
- Team/Application being assessed
- Interview date (YYYY-MM-DD format)
- Team lead name
- Contributors/participants

**Store this information for CSV header generation.**

## Step 2: Application Risk Profile Assessment (D-TA-A)

**Introduction:**
"We'll now assess your Application Risk Profile practices. This covers how you classify and manage application business risk."

### Question D-TA-A-1-1 (Level 1)
**Ask:** "Do you classify applications according to business risk based on a simple and predefined set of questions?"

**Present these answer choices:**
- A: Yes, most or all of them
- B: Yes, for at least half of the applications
- C: Yes, some of them
- D: No
- E: Not applicable

**Prompt for answer:** "Please type your answer choice (A, B, C, D, or E):"

**Validation:** If user provides invalid input, re-ask with guidance:
"Please enter one of the valid letter options: A, B, C, D, or E. Simply type the letter corresponding to your answer."

**After valid answer, ask:** "Please provide any interview notes or observations about this practice:"

### Question D-TA-A-2-1 (Level 2)
**Ask:** "Do you use centralized and quantified application risk profiles to evaluate business risk?"

**Present these answer choices:**
- A: Yes, most or all of them
- B: Yes, for at least half of the applications
- C: Yes, some of them
- D: No
- E: Not applicable

**Prompt for answer:** "Please type your answer choice (A, B, C, D, or E):"

**After valid answer, ask:** "Please provide any interview notes or observations about this practice:"

### Question D-TA-A-3-1 (Level 3)
**Ask:** "Do you regularly review and update the risk profiles for your applications?"

**Present these answer choices:**
- A: Yes, most or all of them
- B: Yes, for at least half of the applications
- C: Yes, some of them
- D: No
- E: Not applicable

**Prompt for answer:** "Please type your answer choice (A, B, C, D, or E):"

**After valid answer, ask:** "Please provide any interview notes or observations about this practice:"

## Step 3: Practice Area Review and Confirmation

**After completing all 3 D-TA-A questions:**

1. **Display summary:**
   "Application Risk Profile Assessment Complete. Here's your summary:"
   - Question 1: [Answer] - [Notes]
   - Question 2: [Answer] - [Notes]
   - Question 3: [Answer] - [Notes]

2. **Allow edits:**
   "Would you like to edit any of these answers? (yes/no)"
   If yes: "Which question number (1, 2, or 3)?" → Re-ask that question
   Continue until user confirms "no"

3. **Show calculated scores:**
   - Individual question scores (based on answer mapping)
   - Practice area average score
   - Display CSV rows for this practice area

4. **Confirm before proceeding:**
   "Are you ready to proceed to Threat Modeling assessment? (yes/no)"

## Step 4: Threat Modeling Assessment (D-TA-B)

**Introduction:**
"Now we'll assess your Threat Modeling practices. This covers how you identify and manage architectural design flaws."

### Question D-TA-B-1-1 (Level 1)
**Ask:** "Do you identify and manage architectural design flaws with threat modeling?"

**Present these answer choices:**
- A: Yes, most or all of them
- B: Yes, for at least half of the applications
- C: Yes, some of them
- D: No
- E: Not applicable

**Prompt for answer:** "Please type your answer choice (A, B, C, D, or E):"

**After valid answer, ask:** "Please provide any interview notes or observations about this practice:"

### Question D-TA-B-2-1 (Level 2)
**Ask:** "Do you use a standard methodology, aligned on your application risk levels?"

**Present these answer choices:**
- A: Yes, most or all of them
- B: Yes, for at least half of the applications
- C: Yes, some of them
- D: No
- E: Not applicable

**Prompt for answer:** "Please type your answer choice (A, B, C, D, or E):"

**After valid answer, ask:** "Please provide any interview notes or observations about this practice:"

### Question D-TA-B-3-1 (Level 3)
**Ask:** "Do you regularly review and update the threat modeling methodology for your applications?"

**Present these answer choices:**
- A: Yes, most or all of them
- B: Yes, for at least half of the applications
- C: Yes, some of them
- D: No
- E: Not applicable

**Prompt for answer:** "Please type your answer choice (A, B, C, D, or E):"

**After valid answer, ask:** "Please provide any interview notes or observations about this practice:"

## Step 5: Final Practice Area Review

**Repeat the same review process as Step 3 for D-TA-B questions**

## Step 6: CSV Generation

**Generate final CSV file with filename:** `SAMM_ThreatAssessment_[DATE].csv`

**CSV Structure (all columns from original):**
```csv
,SAMM Assessment Interview:  For [Organization],,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,
,Instructions,,,,,,,,,,,,,,,,,,,,,,,,
,Interview an individual based on the questions below organized according to SAMM Business Functions and Security Practices.,,,,,,,,,,,,,,,,,,,,,,,,
,Select the best answer from the multiple choice drop down selections in the answer column.,,,,,,,,,,,,,,,,,,,,,,,,
,"Document additional information such as how and why in the ""Interview Notes"" column.",,,,,,,,,,,,,,,,,,,,,,,,
,The formulas in hidden columns F-H will calculate the scores and update the Rating boxes and other worksheets as needed.,,,,,,,,,,,,,,,,,,,,,,,,
,"Once the interview is complete, go to the ""Scorecard"" sheet and follow instructions.",,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,
,Organization: [Organization Name],,,,,,,,,,,,,,,,,,,,,,,,
,Team/Application: [Team/Application],,,,,,,,,,,,,,,,,,,,,,,,
,Interview Date: [Date],,,,,,,,,,,,,,,,,,,,,,,,
,Team Lead: [Team Lead],,,,,,,,,,,,,,,,,,,,,,,,
,Contributors: [Contributors],,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,
,Design,,,,,,,,,,,,,,,,,,,,,,,,
,Stream,Level,Threat Assessment,,Answer,,,Interview Notes,Rating,,,,,,,,,,,,,,,,
D-TA-A-1-1,Application Risk Profile,1,Do you classify applications according to business risk based on a simple and predefined set of questions?,[Answer],[Answer Text],[Score],[Practice Area Average],[Interview Notes],[Overall Rating],,,,,,,,,,,,,,,,
D-TA-A-2-1,,2,Do you use centralized and quantified application risk profiles to evaluate business risk?,[Answer],[Answer Text],[Score],,[Interview Notes],,,,,,,,,,,,,,,,,
D-TA-A-3-1,,3,Do you regularly review and update the risk profiles for your applications?,[Answer],[Answer Text],[Score],,[Interview Notes],,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,
D-TA-B-1-1,Threat Modeling,1,Do you identify and manage architectural design flaws with threat modeling?,[Answer],[Answer Text],[Score],[Practice Area Average],[Interview Notes],[Overall Rating],,,,,,,,,,,,,,,,
D-TA-B-2-1,,2,"Do you use a standard methodology, aligned on your application risk levels?",[Answer],[Answer Text],[Score],,[Interview Notes],,,,,,,,,,,,,,,,,
D-TA-B-3-1,,3,Do you regularly review and update the threat modeling methodology for your applications?,[Answer],[Answer Text],[Score],,[Interview Notes],,,,,,,,,,,,,,,,,
```

## Scoring Algorithm

**Automatic score assignment based on answers:**
- A (Yes, most or all): 1.0
- B (Yes, at least half): 0.5
- C (Yes, some): 0.25
- D (No): 0.0
- E (Not applicable): 0.0

**Practice area average calculation:**
- D-TA-A Average: (Q1 + Q2 + Q3) / 3
- D-TA-B Average: (Q1 + Q2 + Q3) / 3
- Overall D-TA Rating: (D-TA-A Average + D-TA-B Average) / 2

## Assessment Completion

**Final steps:**
1. Generate and save the CSV file
2. Display completion summary with:
   - Total questions answered: 6
   - Practice area scores: D-TA-A and D-TA-B averages
   - Overall Threat Assessment domain score
   - File location of generated CSV

**Completion message:**
"SAMM Threat Assessment completed successfully! Your assessment has been saved to: SAMM_ThreatAssessment_[DATE].csv"

## Validation and Error Handling

**Answer validation:**
- Only accept A, B, C, D, or E (case insensitive)
- Re-prompt with guidance for invalid entries: "Please type only the letter A, B, C, D, or E"
- Show answer options again if user requests clarification

**Required fields:**
- All organization context fields must be provided
- All 6 questions must be answered
- Interview notes are optional but encouraged

**Data integrity:**
- Validate date format (YYYY-MM-DD)
- Ensure no empty critical fields in CSV output
- Calculate scores consistently across all questions

---

**Success Criteria:** Complete interactive assessment of all 6 SAMM Threat Assessment questions with validated answers, collected interview notes, calculated scores, and generated CSV output following the exact format requirements.