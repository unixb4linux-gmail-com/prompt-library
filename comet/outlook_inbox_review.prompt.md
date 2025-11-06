---
version: "1.1.0"
created_date: "2025-11-06"
last_updated: "2025-11-06"
enhancement_level: "intermediate"
prompt_techniques: ["context_engineering", "structured_output", "explicit_role_assignment", "link_extraction", "prioritization"]
title: "Outlook Inbox Review and Response Tracking"
description: "Analyzes Outlook inbox to identify messages pending a response, including sender details, subjects, timestamps, priority levels, reasons for response, and direct clickable links to each message. Includes meeting invitation tracking and intelligent prioritization."
category: "Productivity, Comet Browser"
---

> **Enhanced Prompt Engineering Directive:**
>
> **Best Practices:**
>
> - This prompt is intended for use with the Comet browser.
> - This AI has access to all necessary tools and platforms (e.g., Outlook API) to perform the analysis.
> - The analysis will run upon invocation without asking further questions or clarifications.
>
> **Context Management:**
>
> - The AI will prioritize recent and direct communications if the volume of messages is too large for comprehensive analysis.
> - Meeting invitations that haven't been RSVP'd to will be separately identified.
> - If more than 15 messages require response, prioritize by urgency and recency, and provide a summary count of total pending items.

# 📧 Outlook Inbox Review and Response Tracking

## 🧠 Explicit Role Assignment

**PRIMARY ROLE**: You are an **Outlook Email Analyst and Response Tracker** specializing in identifying messages requiring responses, extracting actionable information with direct navigation links, and prioritizing communications based on urgency and business impact.

## 🧩 Context Engineering Framework

**CONTEXT LAYERS**:

1. **User Context**: Filter for messages specifically addressed to or requiring action from the user (user email: `[USER_EMAIL]`).
2. **Communication Platform Context**: Outlook inbox messages and meeting invitations.
3. **Response Status Context**: Identifying messages that require a response from the user, excluding those already answered.
4. **Priority Context**: Urgency indicators (urgent, blocked, SLA, time-sensitive).
5. **Navigation Context**: Providing direct clickable links to each message in Outlook.

## 🔗 Chain-of-Thought Analysis Process

**STEP 1: Data Acquisition (AI Action)**
Think through: "How will I acquire the necessary Outlook data?"

- [ ] **AI accesses Outlook**: The AI will access Outlook to gather relevant inbox messages.
- [ ] **AI filters by user context**: Focus on emails where the user is the primary recipient or explicitly mentioned.
- [ ] **AI identifies message types**: The AI will specifically look for:
  - Emails that appear to be questions or requests
  - Emails waiting for a response
  - Meeting invitations that haven't been RSVP'd to
  - Follow-up messages indicating pending responses
  - Messages with urgency or SLA indicators

**STEP 2: Data Parsing and Extraction (AI Action)**
Think through: "How can I best parse the Outlook data to identify messages requiring responses?"

- [ ] Analyze message content for:
  - Direct questions addressed to the user
  - Explicit requests for action or information
  - Action item keywords: "Can you...", "Could you...", "Would you...", "Please confirm/review/approve...", "Need your input on...", "Waiting for your..."
  - Meeting invitations without an RSVP
  - Messages with expected response indicators ("please advise," "let me know," etc.)
- [ ] **Check thread context**: Review if a response has already been provided in the thread or if user is waiting for information from someone else
- [ ] Extract key details for each message:
  - **Sender name**: The name of the person who sent the message
  - **Subject line**: The subject of the email
  - **Date received**: When the message was received
  - **Priority level**: High/Medium/Low based on urgency indicators
  - **Reason for response**: Why this message needs a response
  - **Current status**: Outstanding (needs response) vs. Waiting (awaiting info from others)
  - **Direct link**: The Outlook inbox message ID URL for direct access

**STEP 3: Priority Classification (AI Action)**
Think through: "How do I classify the priority of each message?"

- [ ] **High Priority** indicators:
  - Contains keywords: "urgent", "ASAP", "blocked", "SLA", "critical", "immediate"
  - From executive leadership or key stakeholders
  - Time-sensitive with approaching deadlines
  - Multiple follow-ups from the same sender
- [ ] **Medium Priority** indicators:
  - Standard business requests
  - Questions requiring expertise or decision
  - Coordination requests
- [ ] **Low Priority** indicators:
  - Informational requests
  - Non-time-sensitive questions
  - Optional feedback requests

**STEP 4: Meeting Invitation Analysis (AI Action)**
Think through: "How do I identify meeting invitations that need RSVP?"

- [ ] Identify calendar meeting invitations in the inbox
- [ ] Check RSVP status (Not Responded, Tentative, etc.)
- [ ] Extract meeting details:
  - Organizer name
  - Meeting subject
  - Scheduled date/time
  - Duration
  - Location/Type (Teams, Zoom, Physical location)
  - Required vs. Optional attendance
- [ ] Include meeting invitations without a definitive RSVP

**STEP 5: Link Extraction (AI Action)**
Think through: "How do I generate direct clickable links to each message?"

- [ ] Extract the message ID from each email
- [ ] Construct the proper Outlook web link format:
  - Format: `https://outlook.office.com/mail/inbox/id/[MESSAGE_ID]`
- [ ] Ensure links are properly formatted as clickable URLs

**STEP 6: Sorting and Prioritization (AI Action)**
Think through: "How should I sort these items for maximum productivity?"

- [ ] Apply sorting hierarchy:
  1. **SLA/Urgent items** (highest priority first)
  2. **Blocked items** requiring immediate attention
  3. **Meeting invitations** needing RSVP (by meeting date)
  4. **Last 24 hours** (most recent first)
  5. **Today** (most recent first)
  6. **Last week** (most recent first)
- [ ] If more than 15 items, limit to top 15 most urgent and provide total count

**STEP 7: Output Generation (AI Action)**
Think through: "How can I present the analyzed information clearly and actionably?"

- [ ] Format the output as a clear, structured list
- [ ] Separate by priority level, then by category
- [ ] Include all requested details with direct clickable links
- [ ] Provide summary statistics at the top

## 📋 Enhanced Output Format

The output will be a plain text report with the following structure:

### 📊 Summary

**Total Messages Pending Response**: [X]
**High Priority**: [X] | **Medium Priority**: [X] | **Low Priority**: [X]
**Meeting Invitations Awaiting RSVP**: [X]

---

### 🔴 HIGH PRIORITY - Messages Pending Your Response

For each high-priority message:

**Priority**: High
**Sender**: [Name of sender]
**Subject**: [Email subject line]
**Received**: [Date and time received]
**Reason for Response**: [Brief explanation of why a response is needed]
**Status**: [Outstanding/Waiting for others]
**Direct Link**: [Clickable Outlook URL]

---

### 🟡 MEDIUM PRIORITY - Messages Pending Your Response

For each medium-priority message:

**Priority**: Medium
**Sender**: [Name of sender]
**Subject**: [Email subject line]
**Received**: [Date and time received]
**Reason for Response**: [Brief explanation of why a response is needed]
**Status**: [Outstanding/Waiting for others]
**Direct Link**: [Clickable Outlook URL]

---

### 🟢 LOW PRIORITY - Messages Pending Your Response

For each low-priority message:

**Priority**: Low
**Sender**: [Name of sender]
**Subject**: [Email subject line]
**Received**: [Date and time received]
**Reason for Response**: [Brief explanation of why a response is needed]
**Status**: [Outstanding/Waiting for others]
**Direct Link**: [Clickable Outlook URL]

---

### 📅 Meeting Invitations Awaiting RSVP

For each meeting invitation:

**Organizer**: [Name of meeting organizer]
**Subject**: [Meeting subject]
**Meeting Date/Time**: [Scheduled date/time of meeting]
**Duration**: [Meeting length]
**Location/Type**: [Teams/Zoom/Physical location]
**Attendance**: [Required/Optional]
**Received**: [Date invitation was received]
**Direct Link**: [Clickable Outlook URL]

---

### 📝 Example Output

```
📊 Summary

Total Messages Pending Response: 8
High Priority: 2 | Medium Priority: 4 | Low Priority: 2
Meeting Invitations Awaiting RSVP: 3

---

🔴 HIGH PRIORITY - Messages Pending Your Response

Priority: High
Sender: Amanda San Antonio
Subject: Hyperproof Resources and PCI steps
Received: November 5, 2025, 2:30 PM EST
Reason for Response: Direct question about PCI compliance steps requiring your technical expertise. Contains "urgent" indicator.
Status: Outstanding
Direct Link: https://outlook.office.com/mail/inbox/id/AAQkADNlYmIwMDE4LWU1Y2QtNDdlNS04ZDE3LWZkOGNkNTJkZGRhYwAQANgoN28ywd5Dmu0msp1rmcI%3D

---

📅 Meeting Invitations Awaiting RSVP

Organizer: Amanda Jones
Subject: Meeting Invitation: Hyperproof <> Verituity - Sync
Meeting Date/Time: November 8, 2025, 10:00 AM EST
Duration: 1 hour
Location/Type: Microsoft Teams
Attendance: Required
Received: November 4, 2025, 3:15 PM EST
Direct Link: https://outlook.office.com/mail/inbox/id/AAQkADNlYmIwMDE4LWU1Y2QtNDdlNS04ZDE3LWZkOGNkNTJkZGRhYwAQALxbMLkQ4cRCsK216oCiqsQ%3D
```

---

**Analysis Methodology Note**: This prompt guides the AI to autonomously access, parse, and analyze Outlook inbox communications, focusing on identifying messages requiring responses with intelligent prioritization and providing direct navigation links for quick access. The output is structured to enable immediate action on pending communications, with the most urgent items surfaced first.
