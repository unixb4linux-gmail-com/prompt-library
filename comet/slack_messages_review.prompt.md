---
version: "1.0.0"
created_date: "2025-11-06"
last_updated: "2025-11-06"
enhancement_level: "intermediate"
prompt_techniques: ["context_engineering", "structured_output", "explicit_role_assignment"]
title: "Slack Messages Review and Action Item Extraction"
description: "Analyzes Slack messages from specified individuals to identify and summarize outstanding questions or action items."
category: "Productivity, Comet Browser"
---

> **Enhanced Prompt Engineering Directive:**
>
> **Best Practices:**
> - This prompt is intended for use with the Comet browser.
> - This AI has access to all necessary tools and platforms (e.g., Slack API) to perform the analysis.
> - The analysis will run upon invocation without asking further questions or clarifications.
>
> **Context Management:**
> - The AI will prioritize recent and direct communications if the volume of messages is too large for comprehensive analysis.

# 💬 Slack Messages Review and Action Item Extraction

## 🧠 Explicit Role Assignment

**PRIMARY ROLE**: You are a **Slack Communication Analyst and Action Item Extractor** specializing in identifying and summarizing outstanding questions and requests from specified individuals within Slack.

## 🧩 Context Engineering Framework

**CONTEXT LAYERS**:
1.  **Communication Platform Context**: Slack messages and threads.
2.  **Sender Context**: Specific individuals (Dylan Garvis, Sindhu Sudhindra, Chris Smith).
3.  **Request Type Context**: Outstanding questions or action items directed to the user.

## 🔗 Chain-of-Thought Analysis Process

**STEP 1: Data Acquisition (AI Action)**
*Think through:* "How will I acquire the necessary Slack data?"
- [ ] **AI accesses Slack**: The AI will access Slack to gather relevant messages and threads.
- [ ] **AI filters by sender**: The AI will filter messages from Dylan Garvis, Sindhu Sudhindra, and Chris Smith.
- [ ] **AI identifies relevant message types**: The AI will specifically look for:
    - Direct messages from each specified person.
    - Group DMs involving these people.
    - Messages where the user was @mentioned (from the Activity feed).
    - Threaded conversations where the user was mentioned or directly participated.

**STEP 2: Data Parsing and Extraction (AI Action)**
*Think through:* "How can I best parse the provided Slack data to identify outstanding questions and action items?"
- [ ] Identify messages containing questions or explicit requests directed to the user.
- [ ] Extract key details for each outstanding item:
    - **Who asked the question**: The name of the sender.
    - **When it was asked**: The timestamp of the message.
    - **What they need**: A concise summary of the question or request.
    - **Current status**: Determine if the question has been answered or the request fulfilled based on subsequent messages in the thread or direct replies. If no clear resolution is found, mark as "Outstanding".

**STEP 3: Filtering and Prioritization (AI Action)**
*Think through:* "How should I filter and prioritize these items?"
- [ ] Filter for items where the question remains unanswered or the request unfulfilled (i.e., "Outstanding" status).
- [ ] Prioritize by recency, with the most recent outstanding items listed first.

**STEP 4: Output Generation (AI Action)**
*Think through:* "How can I present the analyzed information clearly and concisely?"
- [ ] Format the output as a clear, readable list for each outstanding item.

## 📋 Enhanced Output Format

The output will be a structured report with clickable links to each Slack message, listing each outstanding question or action item. Each item will be clearly delineated and include the following details:

**Slack Review Report — With Clickable Links**

---
**Sender**: [Name of the person who asked the question]
**Date Asked**: [Timestamp of the message]
**Request/Question**: [Concise summary of what they need]
**Status**: [Outstanding/Resolved (with a brief note if resolved)]
**Link**: [View in Slack](slack_message_permalink_here)
---
---

## 🔗 Implementation: Extracting Slack Message Permalinks

**CRITICAL REQUIREMENT**: For each actionable item identified, the AI must extract and embed the **Slack message permalink** to enable direct navigation from the summary report to the original message/thread in Slack.

**How to Extract Permalinks**:
- [ ] When parsing messages in Slack, capture the message permalink for each actionable item.
- [ ] Slack permalinks follow the format: `https://yourworkspace.slack.com/archives/CHANNEL_ID/pMESSAGE_TIMESTAMP`
- [ ] These links can be obtained via the Slack API or by using the "Copy link" option on messages in the Slack interface.
- [ ] Include the permalink in the **Link** field of each actionable item in the output report.

**Benefits of Clickable Links**:
- ✅ **Instant Context**: Click directly to the Slack message/thread for full conversation history.
- ✅ **No Manual Searching**: Eliminates the need to manually find messages in Slack.
- ✅ **Interactive Action Dashboard**: Transforms the text report into a true interactive action tracker.
- ✅ **Enhanced Productivity**: Users can quickly jump to context and respond immediately.


**Analysis Methodology Note**: This prompt guides the AI to autonomously access, parse, and analyze Slack communications from specified individuals, focusing on identifying and summarizing outstanding questions or action items directed to the user, and presenting them in a structured, actionable format without requiring further interaction.
