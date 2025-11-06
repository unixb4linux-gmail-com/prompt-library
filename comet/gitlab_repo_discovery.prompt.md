| version | created_date | last_updated | enhancement_level | prompt_techniques | title | description | category |
|---------|--------------|--------------|-------------------|-------------------|-------|-------------|----------|
| 1.0.0 | 2025-11-06 | 2025-11-06 | intermediate | context_engineering structured_output explicit_role_assignment link_extraction filtering comparison deduplication | GitLab Repository Discovery | Discovers all accessible repositories in specific GitLab organization groups updated within the last 30 days, compares against a known list of cloned repos, and provides SSH clone URLs for new repositories. | DevOps, Productivity, Comet Browser |

> **Enhanced Prompt Engineering Directive:**
>
> **Best Practices:**
> - • This prompt is intended for exclusive use with the Comet browser.
> - • This AI has access to all necessary tools and platforms to perform the analysis (GitLab dashboard access).
> - • The analysis will run upon invocation without asking further questions.
> - • Focus on identifying new repositories not in the known list.
>
> **Context Management:**
> - • The AI will navigate to the GitLab dashboard projects page.
> - • Filter for repositories in the specified organization groups (verituity/verituity-platform and verituity/devops).
> - • Identify repositories updated in the last 30 days.
> - • Compare against the provided list of already cloned repositories.

# 🔍 GitLab Repository Discovery

## 🧠 Explicit Role Assignment

**PRIMARY ROLE**: You are a **GitLab Repository Discovery Specialist** tasked with identifying all accessible repositories within specific organization groups, filtering by recent activity, and comparing against a known baseline to surface new repositories requiring local cloning.

## 🧩 Context Engineering Framework

**CONTEXT LAYERS**:

1. **User Context**: User = the authenticated GitLab user accessing the dashboard
2. **Organization Context**: Target groups = verituity/verituity-platform and verituity/devops
3. **Time Context**: Repositories with commits/updates in the last 30 days
4. **Baseline Context**: List of already cloned repositories to exclude from results
5. **Output Context**: SSH clone URLs for easy repository cloning

## 🔗 Chain-of-Thought Analysis Process

### **STEP 1: Navigation and Access (AI Action)**

Think through: "How will I access the GitLab repository list?"

- [ ] **AI navigates to GitLab**: Go to https://gitlab.com/dashboard/projects
- [ ] **AI authenticates**: Ensure user is logged in and has access to target groups
- [ ] **AI verifies access**: Confirm visibility of verituity organization repositories

### **STEP 2: Repository Filtering (AI Action)**

Think through: "How do I filter for the target repositories?"

- [ ] **Filter by organization groups**:
  - ◦ Target group 1: verituity/verituity-platform
  - ◦ Target group 2: verituity/devops
- [ ] **Filter by activity timeframe**: Last 30 days (updated since November 6, 2025 - 30 days)
- [ ] **Extract all matching repositories**: Scroll through results to capture complete list
- [ ] **Handle pagination**: Ensure all pages of results are processed

### **STEP 3: Data Extraction (AI Action)**

Think through: "What information do I need from each repository?"

- [ ] Extract key details for each repository:
  - ◦ **Repository name**: Short name of the repository
  - ◦ **Full path**: Complete path including group/subgroup structure
  - ◦ **Last commit date**: Most recent update timestamp
  - ◦ **SSH clone URL**: The git clone command URL (git@gitlab.com:...)
  - ◦ **Description**: Brief repository description if available

### **STEP 4: Comparison Against Known List (AI Action)**

Think through: "Which repositories are NOT in the already-cloned list?"

**Known Cloned Repositories**:
- admin-funnel
- admin-workbench-ui
- argocd
- arm-backups
- auth-app
- beneficiary-registry-ui
- boa-test
- build-tools
- cicd-templates
- citi-adapter
- common
- common-core
- common-ui
- configs
- configs-az-keyvault
- funnel
- gitlab-review-agent
- gitops-boa
- golang-sandbox
- iac-gitlab-devops
- iac-gitlab-verituity-platform
- keycloak-ciam-adapter
- lexisnexis-trueid-ui
- minikube
- misc-scripts
- notification-service
- onboarding-portal
- payment-service
- service-protos
- sql-init-scripts
- user-portal-ui
- user-profile

- [ ] **Compare repository names**: Match each discovered repository against the known list
- [ ] **Identify new repositories**: Flag any repositories NOT in the known list
- [ ] **Extract SSH URLs**: For new repositories only, extract the SSH clone URL

### **STEP 5: SSH Clone URL Formatting (AI Action)**

Think through: "How do I provide the SSH clone URLs?"

- [ ] Extract or construct the SSH clone URL format:
  - ◦ Standard format: `git@gitlab.com:[group]/[subgroup]/[repo-name].git`
  - ◦ Example: `git@gitlab.com:verituity/verituity-platform/new-service.git`
- [ ] Ensure URLs are properly formatted and copy-pasteable
- [ ] Verify SSH URLs are accessible (check visibility/permissions if possible)

### **STEP 6: Output Generation (AI Action)**

Think through: "How should I present this information for maximum usability?"

- [ ] Separate results into two sections:
  - ◦ **All Active Repositories**: Complete list of repos with activity in last 30 days
  - ◦ **NEW Repositories**: Only repos NOT in the known cloned list
- [ ] Format output as structured tables with clear indicators
- [ ] Provide summary statistics
- [ ] Include ready-to-use git clone commands

## 📋 Enhanced Output Format

The output will be a comprehensive repository discovery report with the following structure:

### GitLab Repository Discovery Report

**Generated**: [Timestamp]  
**User**: [GitLab Username]  
**Target Groups**: verituity/verituity-platform, verituity/devops  
**Activity Window**: Last 30 days (since [Date])  

#### 📊 Summary

- • **Total Active Repositories**: [Count]
  - ◦ In verituity/verituity-platform: [Count]
  - ◦ In verituity/devops: [Count]
- • **Already Cloned**: [Count]
- • **🆕 NEW Repositories Requiring Clone**: [Count]

#### 🆕 NEW REPOSITORIES - Requiring Local Clone

| Repository Name | Full Path | Last Commit Date | SSH Clone URL |
|-----------------|-----------|------------------|---------------|
| [new-repo-1] | verituity/group/new-repo-1 | 2025-11-05 | `git@gitlab.com:verituity/group/new-repo-1.git` |
| [new-repo-2] | verituity/devops/new-repo-2 | 2025-11-03 | `git@gitlab.com:verituity/devops/new-repo-2.git` |

**Quick Clone Commands**:
```bash
# Clone all new repositories
git clone git@gitlab.com:verituity/group/new-repo-1.git
git clone git@gitlab.com:verituity/devops/new-repo-2.git
```

---

#### 📚 ALL ACTIVE REPOSITORIES - Last 30 Days

| Repository Name | Full Path | Last Commit Date | Status |
|-----------------|-----------|------------------|--------|
| [repo-name] | verituity/group/repo-name | 2025-11-06 | ✅ Already Cloned |
| [new-repo-1] | verituity/group/new-repo-1 | 2025-11-05 | 🆕 NEW |
| [repo-name-2] | verituity/devops/repo-name-2 | 2025-11-04 | ✅ Already Cloned |

## 🔍 Detailed Discovery Guidelines

### What to Look For:

1. **Target Organization Groups**:
   - ◦ verituity/verituity-platform (and all subgroups)
   - ◦ verituity/devops (and all subgroups)
   - ◦ Include all nested subgroup repositories

2. **Activity Indicators**:
   - ◦ Last commit date within 30 days
   - ◦ Last updated/modified timestamp
   - ◦ Recent merge requests or activity

3. **Repository Details to Extract**:
   - ◦ Repository name (short name)
   - ◦ Full path including group hierarchy
   - ◦ Last commit/update date
   - ◦ SSH clone URL
   - ◦ Repository description (if available)
   - ◦ Visibility level (private/internal/public)

### Filtering Logic:

**INCLUDE** repositories that:
- • Belong to verituity/verituity-platform or verituity/devops groups
- • Have been updated in the last 30 days
- • User has at least read access to

**EXCLUDE** repositories that:
- • Are older than 30 days without recent activity
- • Belong to other organizations
- • Are archived or disabled
- • User doesn't have access to

### Comparison Logic:

**When comparing against the known cloned list**:
- • Use repository name for matching (short name, not full path)
- • Be case-sensitive in matching
- • Mark as NEW if:
  - ◦ Repository name is not in the known list
  - ◦ Repository appears to be a renamed version
  - ◦ Repository is in a new subgroup structure

### SSH Clone URL Format:

**Standard SSH URL pattern**:
```
git@gitlab.com:[organization]/[group]/[subgroup]/[repo-name].git
```

**Examples**:
- `git@gitlab.com:verituity/verituity-platform/new-api-service.git`
- `git@gitlab.com:verituity/devops/monitoring-tools.git`
- `git@gitlab.com:verituity/verituity-platform/frontend/new-ui-component.git`

## 🎯 Key Success Criteria

1. **Completeness**: All repositories in target groups with activity in last 30 days are identified
2. **Accuracy**: NEW repositories are correctly identified by comparing against the known list
3. **Actionability**: SSH clone URLs are provided in ready-to-use format
4. **Clarity**: Clear distinction between already-cloned and new repositories
5. **Efficiency**: Report is concise yet comprehensive

**Analysis Methodology Note**: This prompt guides the AI to autonomously access GitLab's project dashboard, filter repositories by organization groups and recent activity, compare against a baseline list of cloned repositories, and output new repositories with their SSH clone URLs for immediate action. The focus is on discovering gaps in local repository coverage and enabling quick synchronization.
