# Terraform Module Documentation Generator

## Purpose
Guide users (or Copilot Chat) to auto-generate documentation for Terraform modules, including variables, outputs, and usage examples.

## Instructions
- Analyze the Terraform module directory for `variables.tf`, `outputs.tf`, and main resources.
- Extract all input variables and outputs with descriptions and types.
- Generate a markdown table for variables and outputs.
- Provide a usage example with required variables.
- Optionally, include a prompt for ChatGPT to generate a README.

## Examples

### Prompt for Copilot/ChatGPT
```
Analyze this Terraform module and generate documentation with:
- A summary of the module's purpose
- A table of input variables (name, type, description, default)
- A table of outputs (name, description)
- A usage example
```

### Example Output
```markdown
## Example: S3 Bucket Module

### Variables
| Name         | Type   | Description         | Default |
|--------------|--------|---------------------|---------|
| bucket_name  | string | Name of the bucket  | n/a     |
| versioning   | bool   | Enable versioning   | false   |

### Outputs
| Name         | Description           |
|--------------|----------------------|
| bucket_arn   | ARN of the bucket    |
| bucket_name  | Name of the bucket   |

### Usage
```hcl
module "s3_bucket" {
  source      = "./modules/s3-bucket"
  bucket_name = "my-bucket"
  versioning  = true
}
```
```
