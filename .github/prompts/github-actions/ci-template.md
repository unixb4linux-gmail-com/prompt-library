# GitHub Actions CI Workflow Template for Containerized Apps

## Purpose
Help users scaffold a GitHub Actions CI workflow to build, push, and deploy containerized applications. Includes Azure and Azure Container Registry (ACR) integration.

## Instructions
- Copy the YAML snippets into your `.github/workflows/` directory.
- Replace placeholders (e.g., `<IMAGE_NAME>`, `<ACR_NAME>`, `<AZURE_WEBAPP_NAME>`, `<RESOURCE_GROUP>`) with your values.
- Add or modify steps as needed for your stack.

## Examples

### Basic CI/CD Workflow
```yaml
name: CI/CD
on:
  push:
    branches: [ main ]
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Log in to Azure
        uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      - name: Log in to ACR
        uses: azure/docker-login@v2
        with:
          login-server: <ACR_NAME>.azurecr.io
          username: ${{ secrets.ACR_USERNAME }}
          password: ${{ secrets.ACR_PASSWORD }}
      - name: Build and push Docker image
        run: |
          docker build -t <ACR_NAME>.azurecr.io/<IMAGE_NAME>:${{ github.sha }} .
          docker push <ACR_NAME>.azurecr.io/<IMAGE_NAME>:${{ github.sha }}
      - name: Deploy to Azure Web App
        uses: azure/webapps-deploy@v3
        with:
          app-name: <AZURE_WEBAPP_NAME>
          images: <ACR_NAME>.azurecr.io/<IMAGE_NAME>:${{ github.sha }}
```

### Reusable YAML Snippet: Build & Push
```yaml
- name: Build and push Docker image
  run: |
    docker build -t <ACR_NAME>.azurecr.io/<IMAGE_NAME>:${{ github.sha }} .
    docker push <ACR_NAME>.azurecr.io/<IMAGE_NAME>:${{ github.sha }}
```

### Reusable YAML Snippet: Azure Login
```yaml
- name: Log in to Azure
  uses: azure/login@v2
  with:
    creds: ${{ secrets.AZURE_CREDENTIALS }}
```

## References
- [GitHub Actions for Azure](https://github.com/Azure/actions)
- [Azure Container Registry Docs](https://learn.microsoft.com/en-us/azure/container-registry/)
