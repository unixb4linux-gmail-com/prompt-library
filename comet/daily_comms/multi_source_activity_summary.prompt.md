---
version: 1.0
name: Multi-Source Activity & Completion Summary
description: Comprehensive work activity summary across all platforms with time-based organization
tags: [productivity, communication, workflow, reporting, status]
author: prompt-library
created: 2025-11-12
---

# Multi-Source Activity & Completion Summary

## Purpose
Provide a comprehensive, deduplicated summary of recent work activities, accomplishments, and completions across all communication and development platforms.

## Instructions

### Data Sources
Aggregate and review activity from the following platforms:

1. **Email Systems**
   - Outlook Inbox (review/action items, sent items)
   - Gmail Inbox (review/action items, sent items)

2. **Calendar Systems**
   - Outlook Calendar (meetings, RSVPs, scheduled events)
   - Google Calendar (meetings, RSVPs, scheduled events)

3. **Communication Platforms**
   - Microsoft Teams (messages, mentions, threads, calls)
   - Slack (messages, mentions, channels, DMs, threads)

4. **Task & Project Management**
   - Jira (tickets assigned, completed, commented, blocked)
   - Confluence (page edits, comments, creations)

5. **Code Repositories**
   - GitHub (PRs, issues, commits, merges, comments, reviews)
   - GitLab (MRs, issues, commits, merges, comments, reviews)

### Time Buckets
Organize all activity into three chronological sections:
- **Last 24 Hours** (since yesterday at this time)
- **This Week** (past 7 days)
- **Last Two Weeks** (past 14 days)

### Processing Rules

1. **Deduplication**: When the same item appears across multiple platforms (e.g., Jira ticket mentioned in Slack and email), consolidate into a single entry with all source references.

2. **Status Classification**:
   - ✅ **Completed**: Finished, merged, closed, resolved
   - 🔄 **In Progress**: Active work, open PRs, ongoing discussions
   - ⏸️ **Waiting**: Pending review, awaiting input, blocked
   - 🚨 **Blocked**: Explicitly blocked with identified blocker

3. **Priority Indicators** (when determinable):
   - 🔴 High/Urgent
   - 🟡 Medium/Normal  
   - 🟢 Low

### Output Format

For each time bucket, provide a structured table with these columns:

| Status | Type | Summary | Source(s) | Date/Time | Priority | Link(s) |
|--------|------|---------|-----------|-----------|----------|--------|

**Column Definitions**:
- **Status**: Use emoji indicators (✅🔄⏸️🚨)
- **Type**: PR, MR, Issue, Ticket, Meeting, Email, Message, Comment, etc.
- **Summary**: Brief description of the activity or accomplishment
- **Source(s)**: Platform name(s), deduplicated
- **Date/Time**: Timestamp of activity
- **Priority**: Priority level if known
- **Link(s)**: Direct clickable URLs to source items

### Execution Steps

1. **Connect to all data sources** using available credentials and access
2. **Extract activities** where I am:
   - Author/creator
   - Assignee
   - Participant/attendee
   - Mentioned/tagged
   - Reviewer/commenter
3. **Filter by timeframe** for each bucket
4. **Deduplicate** cross-platform references
5. **Classify status** for each item
6. **Sort** by recency within each time bucket (most recent first)
7. **Generate output** in table format

### Special Focus Areas

#### Accomplishments & Completions
- Highlight merged PRs/MRs
- Closed tickets and issues
- Completed projects or milestones
- Resolved blockers
- Successful deployments

#### Action Items & Follow-ups
- Outstanding questions in messages
- Pending reviews (requested from me)
- Overdue tasks
- Unanswered emails requiring response

#### Blockers & Risks
- Explicitly blocked items
- Items waiting >3 days
- Failed builds or tests
- Unresolved critical issues

## Example Output

### Last 24 Hours

| Status | Type | Summary | Source(s) | Date/Time | Priority | Link(s) |
|--------|------|---------|-----------|-----------|----------|--------|
| ✅ | PR | Merged azure-mlops authentication patch | GitHub | Nov 12, 10:15 AM | 🔴 | [PR #456](link) |
| ✅ | Ticket | Closed VAULT-123: SFTP alerting implementation | Jira, Slack | Nov 12, 9:30 AM | 🟡 | [JIRA](link), [Slack](link) |
| 🔄 | Review | Reviewed security scanning PR, requested changes | GitHub | Nov 12, 8:45 AM | 🟡 | [PR #457](link) |
| ✅ | Email | Responded to compliance audit questions | Outlook | Nov 12, 8:20 AM | 🔴 | [Email](link) |
| 🔄 | Meeting | Sprint planning (attended) | Teams, Outlook | Nov 12, 2:00 PM | 🟡 | [Meeting](link) |

### This Week

| Status | Type | Summary | Source(s) | Date/Time | Priority | Link(s) |
|--------|------|---------|-----------|-----------|----------|--------|
| ✅ | PR | Merged database migration hotfix | GitHub | Nov 11, 4:30 PM | 🔴 | [PR #455](link) |
| 🔄 | Issue | Investigating performance degradation | GitHub, Slack | Nov 11, 2:15 PM | 🟡 | [Issue #789](link) |
| ✅ | Ticket | Completed API documentation update | Jira, Confluence | Nov 10, 3:45 PM | 🟢 | [JIRA](link), [Docs](link) |
| ⏸️ | PR | Waiting on QA approval for feature branch | GitLab | Nov 9, 11:00 AM | 🟡 | [MR !234](link) |

### Last Two Weeks

| Status | Type | Summary | Source(s) | Date/Time | Priority | Link(s) |
|--------|------|---------|-----------|-----------|----------|--------|
| ✅ | Release | Deployed v2.4.0 to production | GitHub, Slack | Nov 5, 9:00 AM | 🔴 | [Release](link) |
| ✅ | Ticket | Resolved 5 security vulnerabilities | Jira | Nov 4, 2:30 PM | 🔴 | [JIRA](link) |
| 🔄 | Epic | Refactoring authentication service (ongoing) | Jira, GitHub | Nov 3, started | 🟡 | [Epic](link) |

## Summary Statistics

Provide a brief statistical overview:

```
📊 Activity Summary (Last 24 Hours)
- ✅ Completed: 4
- 🔄 In Progress: 2
- ⏸️ Waiting: 0
- 🚨 Blocked: 0

📊 Activity Summary (This Week)
- ✅ Completed: 12
- 🔄 In Progress: 8
- ⏸️ Waiting: 3
- 🚨 Blocked: 1

📊 Activity Summary (Last Two Weeks)
- ✅ Completed: 28
- 🔄 In Progress: 15
- ⏸️ Waiting: 5
- 🚨 Blocked: 2
```

## Output Guidelines

1. **Be Concise**: Summaries should be 1-2 sentences maximum
2. **Avoid Noise**: Filter out routine/automated items (unless significant)
3. **Highlight Value**: Focus on accomplishments and actionable items
4. **Maintain Context**: Include enough detail to understand significance
5. **Preserve Links**: Always include direct URLs for easy navigation
6. **Update Regularly**: This summary is meant for daily/weekly review

## Role Context

You are an expert productivity aggregator and analyst. Your goal is to provide a clear, actionable dashboard of recent work activity that:
- Surfaces accomplishments for status reporting
- Identifies outstanding action items
- Highlights blockers requiring attention
- Eliminates duplicate entries across platforms
- Saves time by centralizing multi-source information

## Notes

- **Authentication**: Ensure proper access to all listed platforms
- **Privacy**: Respect confidential/private content restrictions
- **Timeliness**: Use current timestamp as reference point
- **Accuracy**: Verify deduplicated items actually refer to the same work
- **Adaptability**: Adjust sources list based on user's actual toolset
