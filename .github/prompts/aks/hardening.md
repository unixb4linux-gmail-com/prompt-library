# AKS Security Hardening Checklist

## Purpose

Guide users through security hardening of Azure Kubernetes Service (AKS) 
clusters using industry best practices. This checklist ensures robust security 
posture, compliance, and integration with NGINX and Cloudflare.

## Instructions

- Review each item in the checklist and apply as appropriate to your AKS 
  environment.
- Use the provided commands and links for reference.
- For NGINX and Cloudflare, follow the integration steps at the end.

## Checklist

- [ ] Enforce TLS 1.2 or higher for all ingress and API endpoints
- [ ] Enable and configure RBAC (Role-Based Access Control)
- [ ] Enable Azure AD integration for authentication
- [ ] Apply Kubernetes network policies to restrict pod communication
- [ ] Enable Azure Defender for Kubernetes
- [ ] Restrict API server access using authorized IP ranges
- [ ] Use managed identities for pod access to Azure resources
- [ ] Enable private cluster mode (disable public API endpoint)
- [ ] Regularly update node pools and apply security patches
- [ ] Enable audit logging and monitor logs for suspicious activity
- [ ] Use Azure Policy for Kubernetes to enforce security standards
- [ ] Scan container images for vulnerabilities before deployment
- [ ] Limit pod permissions (avoid privileged containers, use 
      PodSecurityPolicies or OPA Gatekeeper)
- [ ] Encrypt secrets at rest using customer-managed keys
- [ ] Enable automatic scaling and resource limits for workloads

## NGINX and Cloudflare Integration

### NGINX Ingress Controller

- Deploy NGINX Ingress Controller using Helm:

```sh
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install nginx-ingress ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace
```

- Enforce TLS 1.2+ in NGINX config:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/ssl-protocols: "TLSv1.2 TLSv1.3"
...
```

### Cloudflare Integration

- Point your domain's DNS to Cloudflare and configure proxying.
- Set up Cloudflare Origin Certificates and upload to AKS secrets.
- Restrict AKS ingress to accept traffic only from Cloudflare IPs (use 
  network policies or Azure NSGs).
- Enable Web Application Firewall (WAF) and DDoS protection in Cloudflare.

## Examples

- [AKS Security Baseline](https://learn.microsoft.com/en-us/azure/architecture/framework/security/aks-security-baseline)
- [Azure Policy for AKS](https://learn.microsoft.com/en-us/azure/aks/use-azure-policy)
- [NGINX Ingress TLS](https://kubernetes.github.io/ingress-nginx/user-guide/tls/)
- [Cloudflare Origin CA](https://developers.cloudflare.com/ssl/origin-configuration/origin-ca/)
