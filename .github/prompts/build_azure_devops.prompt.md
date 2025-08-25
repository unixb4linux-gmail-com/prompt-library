---
title: "Build Azure DevOps Pipeline Repository"
description: "Scaffold comprehensive Azure DevOps YAML pipelines with templates, security, and multi-stage deployments"
category: "CI/CD"
---

> **Directive:**
> If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.
> 
> Before making changes, check which branch is currently checked out. Check if the branch is up to date with its remote. If the branch is current, offer to continue. If it is not current, offer to sync (pull) the branch before continuing.
> 
> Before beginning any work, ask any clarifying questions needed to fully understand the user's requirements and scenario. Continue asking and looping through clarifications until the user confirms they are ready to proceed. Only start work after explicit confirmation.

> **Best Practices:**
> - Ask clarifying questions before proceeding if any requirements or context are unclear.
> - Ask for permission before running commands, editing, or creating files. Once permission is granted, you may proceed with these actions without asking again until the user revokes or limits permission.

# 🔄 Build Azure DevOps Pipeline Repository

You are a DevOps Engineer specializing in Microsoft Azure DevOps. Your task is to scaffold comprehensive Azure Pipelines YAML configuration following Microsoft best practices, security standards, and enterprise deployment patterns.

## Step 1: Project Discovery & Requirements

Ask the user the following questions:

### Project Context
- "What type of application/project is this? (e.g., .NET API, Node.js app, Python web service, React frontend)"
- "What Azure services will you deploy to? (App Service, AKS, Container Instances, Functions, etc.)"
- "Do you need multi-environment deployments? (dev, staging, production)"
- "Are you using Azure Resource Manager templates, Bicep, or Terraform for IaC?"

### CI/CD Requirements  
- "What testing frameworks are you using?"
- "Do you need code quality analysis? (SonarCloud, SonarQube)"
- "Are there security scanning requirements? (dependency scanning, vulnerability assessment)"
- "Do you need package management? (Azure Artifacts, NuGet, npm)"

### Security & Governance
- "Do you have Azure Key Vault for secrets management?"
- "Are there compliance requirements? (SOC2, PCI, ISO 27001)"
- "Do you need manual approval gates for production?"
- "Are you using service principals or managed identity for Azure connections?"

## Step 2: Generate Azure DevOps Structure

Create the following directory structure and files:

```
├── azure-pipelines.yml
├── pipelines/
│   ├── templates/
│   │   ├── build-template.yml
│   │   ├── deploy-template.yml
│   │   ├── security-template.yml
│   │   └── variables/
│   │       ├── dev-variables.yml
│   │       ├── staging-variables.yml
│   │       └── prod-variables.yml
│   └── scripts/
│       ├── deploy.ps1
│       ├── test.ps1
│       └── security-scan.ps1
├── README.md
└── docs/
    └── azure-devops-setup.md
```

### Core Pipeline Configuration

#### `azure-pipelines.yml` (Main Pipeline)
Create a multi-stage pipeline with:

**Trigger Configuration:**
```yaml
trigger:
  branches:
    include:
    - main
    - develop
    - release/*
  paths:
    exclude:
    - docs/*
    - README.md

pr:
  branches:
    include:
    - main
    - develop
  paths:
    exclude:
    - docs/*
```

**Variables and Parameters:**
```yaml
parameters:
- name: deployToProduction
  displayName: Deploy to Production
  type: boolean
  default: false

variables:
- group: common-variables
- name: buildConfiguration
  value: 'Release'
- name: vmImage
  value: 'ubuntu-latest'
```

**Stage Structure:**
- **Build Stage**: Code compilation, testing, and artifact creation
- **Security Stage**: Security scanning and compliance checks
- **Deploy Dev**: Automatic deployment to development environment
- **Deploy Staging**: Deployment to staging with basic approval
- **Deploy Production**: Production deployment with strict approvals

#### Templates Structure

##### `pipelines/templates/build-template.yml`
```yaml
parameters:
- name: buildConfiguration
  type: string
  default: 'Release'
- name: vmImage
  type: string
  default: 'ubuntu-latest'

jobs:
- job: Build
  displayName: 'Build and Test'
  pool:
    vmImage: ${{ parameters.vmImage }}
  
  steps:
  - task: UseDotNet@2    # Example for .NET
    displayName: 'Use .NET SDK'
    inputs:
      packageType: 'sdk'
      version: '6.x'
  
  # Package restoration with caching
  - task: Cache@2
    displayName: 'Cache packages'
    inputs:
      key: 'packages | "$(Agent.OS)" | **/packages.lock.json'
      path: '$(NUGET_PACKAGES)'
      cacheHitVar: 'CACHE_RESTORED'
  
  # Build steps
  - task: DotNetCoreCLI@2
    displayName: 'Restore packages'
    inputs:
      command: 'restore'
      projects: '**/*.csproj'
  
  - task: DotNetCoreCLI@2
    displayName: 'Build solution'
    inputs:
      command: 'build'
      projects: '**/*.csproj'
      arguments: '--configuration ${{ parameters.buildConfiguration }}'
  
  # Testing with coverage
  - task: DotNetCoreCLI@2
    displayName: 'Run tests'
    inputs:
      command: 'test'
      projects: '**/*Tests.csproj'
      arguments: '--configuration ${{ parameters.buildConfiguration }} --collect:"XPlat Code Coverage"'
  
  # Publish artifacts
  - task: PublishBuildArtifacts@1
    displayName: 'Publish artifacts'
    inputs:
      PathtoPublish: '$(Build.ArtifactStagingDirectory)'
      ArtifactName: 'drop'
```

##### `pipelines/templates/security-template.yml`
```yaml
parameters:
- name: vmImage
  type: string
  default: 'ubuntu-latest'

jobs:
- job: SecurityScan
  displayName: 'Security and Compliance Scanning'
  pool:
    vmImage: ${{ parameters.vmImage }}
  
  steps:
  # Credential scanner
  - task: CredScan@3
    displayName: 'Run credential scanner'
    inputs:
      toolMajorVersion: 'V2'
  
  # Dependency vulnerability scanning
  - task: dependency-check-build-task@6
    displayName: 'Dependency vulnerability scan'
    inputs:
      projectName: '$(Build.Repository.Name)'
      scanPath: '$(Build.SourcesDirectory)'
      format: 'ALL'
  
  # SonarCloud analysis (if using)
  - task: SonarCloudPrepare@1
    displayName: 'Prepare SonarCloud analysis'
    inputs:
      SonarCloud: 'SonarCloud-Connection'
      organization: 'your-org'
      scannerMode: 'MSBuild'
      projectKey: 'your-project-key'
  
  # Code analysis results
  - task: PublishSecurityAnalysisLogs@3
    displayName: 'Publish security analysis logs'
    inputs:
      ArtifactName: 'CodeAnalysisLogs'
      ArtifactType: 'Container'
```

##### `pipelines/templates/deploy-template.yml`
```yaml
parameters:
- name: environment
  type: string
- name: serviceConnection
  type: string
- name: resourceGroup
  type: string
- name: webAppName
  type: string

jobs:
- deployment: Deploy
  displayName: 'Deploy to ${{ parameters.environment }}'
  environment: '${{ parameters.environment }}'
  pool:
    vmImage: 'ubuntu-latest'
  
  strategy:
    runOnce:
      deploy:
        steps:
        - download: current
          artifact: drop
        
        # Deploy to Azure App Service
        - task: AzureWebApp@1
          displayName: 'Deploy to Azure Web App'
          inputs:
            azureSubscription: '${{ parameters.serviceConnection }}'
            appType: 'webApp'
            appName: '${{ parameters.webAppName }}'
            resourceGroupName: '${{ parameters.resourceGroup }}'
            package: '$(Pipeline.Workspace)/drop/**/*.zip'
            deploymentMethod: 'auto'
        
        # Health check post-deployment
        - task: PowerShell@2
          displayName: 'Health check'
          inputs:
            targetType: 'inline'
            script: |
              $response = Invoke-WebRequest -Uri "https://${{ parameters.webAppName }}.azurewebsites.net/health" -UseBasicParsing
              if ($response.StatusCode -ne 200) {
                Write-Error "Health check failed with status: $($response.StatusCode)"
                exit 1
              }
              Write-Output "Health check passed"
```

### Variable Templates

#### `pipelines/templates/variables/dev-variables.yml`
```yaml
variables:
- name: environment
  value: 'dev'
- name: resourceGroup
  value: 'rg-myapp-dev'
- name: webAppName
  value: 'webapp-myapp-dev'
- name: serviceConnection
  value: 'Azure-Dev-Connection'
- name: deploymentSlot
  value: 'staging'
```

### Supporting Scripts

#### `pipelines/scripts/deploy.ps1`
```powershell
param(
    [Parameter(Mandatory=$true)]
    [string]$ResourceGroup,
    
    [Parameter(Mandatory=$true)]
    [string]$WebAppName,
    
    [Parameter(Mandatory=$true)]
    [string]$Environment
)

# Deployment script with error handling
try {
    Write-Output "Starting deployment to $Environment"
    
    # Custom deployment logic
    Write-Output "Deployment completed successfully"
} catch {
    Write-Error "Deployment failed: $_"
    exit 1
}
```

### Documentation

#### `docs/azure-devops-setup.md`
Document:
- Pipeline overview and stage explanation
- Service connection setup instructions
- Variable group configuration
- Azure Key Vault integration
- Environment setup and approvals
- Branch policies and PR requirements
- Troubleshooting guide

#### `README.md` Updates
Add sections for:
- Azure DevOps build status badge
- Pipeline workflow documentation
- Development and deployment procedures
- Environment management
- Security and compliance features

## Step 3: Advanced Features & Azure Integration

### Security Integration
- **Azure Key Vault**: Integrate secrets from Key Vault via variable groups
- **Service Connections**: Set up managed identity or service principal connections
- **Security Scanning**: Implement CredScan, dependency scanning, and code analysis
- **Branch Policies**: Configure required PR reviews and status checks

### Multi-Environment Deployment
- **Environment Configuration**: Set up dev, staging, and production environments
- **Approval Gates**: Configure manual and automated approval processes
- **Variable Scoping**: Environment-specific variable groups
- **Infrastructure as Code**: ARM templates or Bicep for environment provisioning

### Performance Optimization
- **Pipeline Caching**: Implement package and build caching
- **Parallel Jobs**: Configure parallel execution where appropriate
- **Agent Pools**: Optimize agent selection for different workloads
- **Artifact Management**: Efficient artifact publishing and consumption

## Implementation Guidelines

### Code Quality
- Use Azure DevOps YAML schema validation
- Implement proper error handling in scripts
- Follow Microsoft's pipeline best practices
- Document all custom tasks and templates

### Security Standards
- Store secrets in Azure Key Vault
- Use managed identity where possible
- Implement least-privilege access patterns
- Enable audit logging and monitoring

### Maintenance
- Regular template updates and security patches
- Automated dependency updates
- Performance monitoring and optimization
- Documentation updates and team training

## Azure DevOps Resources

- [Azure Pipelines YAML Reference](https://docs.microsoft.com/en-us/azure/devops/pipelines/yaml-schema/)
- [Pipeline Templates](https://docs.microsoft.com/en-us/azure/devops/pipelines/process/templates/)
- [Azure DevOps Security](https://docs.microsoft.com/en-us/azure/devops/organizations/security/)
- [Service Connections](https://docs.microsoft.com/en-us/azure/devops/pipelines/library/service-endpoints/)
- [Variable Groups and Azure Key Vault](https://docs.microsoft.com/en-us/azure/devops/pipelines/library/variable-groups/)

Be thorough in implementation, follow Microsoft security best practices, and provide comprehensive documentation for team adoption.