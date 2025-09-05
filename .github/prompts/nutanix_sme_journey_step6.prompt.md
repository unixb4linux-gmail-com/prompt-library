# Nutanix SME Journey Step 6: Database Service (MySQL)

## Objective
Learn Nutanix Database Service (NDB) for MySQL: provisioning, patching, cloning, and backup/restore.

---

## Instructions to AI
- Ask clarifying questions first (MySQL version, HA needs).  
- Only move forward on `continue`, `next`, or `proceed`.  
- Provide UI workflows, CLI steps should be suggested for Claude.

---

## Steps

### Step 1: Clarify MySQL Needs
- Version, HA/replication, maintenance windows.

### Step 2: Provision MySQL
- Deploy via NDB.  
- Evidence: DB ID, connection string.

### Step 3: Patch Cycle
- Apply patch/upgrade workflow.  
- Evidence: patch log.

### Step 4: Clone DB
- Create a dev/test clone.  
- Evidence: clone ID.

### Step 5: Backup & Restore
- Run a backup.  
- Restore into test environment.  
- Evidence: backup/restore IDs.

---

## Exit Criteria
- One MySQL DB provisioned, patched, cloned, and restored.  
- SLA notes documented.

---

## Quiz
1. Which databases are supported by NDB?  
   - a) MySQL, Postgres, Oracle, SQL Server, MongoDB  
   - b) Only MySQL and Postgres  
   - c) Oracle only  
2. What is a common use of DB cloning?  
   - a) Ransomware detection  
   - b) Dev/test environments  
   - c) Storage expansion  
3. Which step ensures disaster recovery for MySQL?  
   - a) Backup and restore  
   - b) Creating a VM  
   - c) Patching  

---

## Resources
- [Nutanix Database Service](https://www.nutanix.com/products/database-service)  
- [Nutanix NDB MySQL Guide](https://portal.nutanix.com/page/documents/database-service)  
- [Nutanix University – Database Courses](https://www.nutanixuniversity.com/)  
