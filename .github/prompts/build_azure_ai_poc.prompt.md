> **Best Practices:**
> - Ask clarifying questions before proceeding if any requirements or context are unclear.
> - Ask for permission before running commands, editing, or creating files. Once permission is granted, you may proceed with these actions without asking again until the user revokes or limits permission.

You are an expert Azure DevOps engineer.  
Generate the minimal code and deployment scaffolding for a **fast and cheap Azure AI POC** as follows:

## Requirements
1. **Backend**
   - Provide a simple Azure Function (Python or Node) that:
     - Accepts a `/chat` POST request with JSON body `{ "message": "..." }`.
     - Forwards the request to an **Azure AI Foundry endpoint** using endpoint URL + API key stored in environment variables.
     - Returns the model’s reply as JSON `{ "reply": "..." }`.

2. **Frontend**
   - Provide a minimal HTML + JavaScript page that:
     - Shows a text input + “Send” button.
     - Calls the backend `/chat` function with fetch().
     - Displays the returned reply on the page.

3. **Deployment**
   - Include an `azure-static-web-apps.yml` GitHub Actions workflow that:
     - Builds and deploys the static web app frontend + Azure Function backend.
     - Uses free tier where possible.
   - Add infrastructure notes for creating the Azure AI Foundry Project + deploying a Phi-4-mini model endpoint.

4. **Proof**
   - Provide example curl request to `/chat` showing success.
   - Add instructions for environment variables:
     - `AZURE_AI_ENDPOINT`
     - `AZURE_AI_KEY`
     - `AZURE_AI_DEPLOYMENT`

## Constraints
- Keep everything as simple as possible—minimal dependencies.
- Optimize for speed and lowest cost (use Static Web Apps free tier, Functions consumption plan).
- Ensure code is copy-paste ready.

Deliverables:
- `api/chat/index.js` (or `main.py`) for the Function
- `index.html` for the frontend
- `azure-static-web-apps.yml` for GitHub Actions
- README.md with setup steps and sample screenshots/commands
