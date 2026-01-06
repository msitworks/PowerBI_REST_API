# Power BI REST API Automation

## 📌 Project Description

This project is built to automate and streamline operations within the Power BI Service using Power BI REST APIs. It enables programmatic interaction with Power BI workspaces, datasets, reports, and refresh processes, allowing teams to replace repetitive manual actions with reliable, API-driven workflows.

The solution is designed with scalability and maintainability in mind, supporting secure authentication via Azure Active Directory and structured API calls to perform administrative and operational tasks. It can be used to trigger dataset refreshes, monitor refresh status, retrieve metadata, and manage Power BI assets across environments.

By integrating Power BI APIs into automation pipelines, this project helps improve operational efficiency, enforce governance, and support enterprise-grade BI operations. It is suitable for BI administrators, data engineers, and DevOps teams looking to integrate Power BI management into scheduled jobs, CI/CD pipelines, or monitoring frameworks.

## 🎯 Purpose

The purpose of this project is to:
- Automate Power BI operations using REST APIs
- Enable repeatable and scalable automation workflows
- Simplify Power BI administration and monitoring
- Provide a reusable framework for Power BI API integrations

## 🧰 Prerequisites

Before setting up the project, ensure you have:
- Power BI Pro or Premium access
- Azure AD App Registration with Power BI API permissions
- Tenant ID, Client ID, and Client Secret
- Python 3.x installed
- Internet access to Power BI Service

## ⚙️ Setup Steps

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/msitworks/PowerBI_REST_API.git
cd PowerBI_REST_API
```


### 2️⃣ Configure Authentication
Create a configuration file or environment variables with the following details:
```
TENANT_ID=<your-tenant-id>
CLIENT_ID=<your-client-id>
CLIENT_SECRET=<your-client-secret>
```
Ensure the Azure AD App has required permissions such as:
- Dataset.ReadWrite.All
- Report.Read.All
- Workspace.Read.All


### 3️⃣ Install Dependencies
Create a python Environment and install dependencies with below
```
pip install -r requirements.txt
```

*(If requirements.txt is not present, install requests and related libraries manually.)*


## ▶️ Run Steps

### 📊 Execute Automation

Run the main automation script to trigger Power BI API operations:
```
python app.py xxxxx yyyyy

```
replace xxxxx with workspaceId
and yyyyy with DatasetID

both are positional Arguments

## 📚 References

- Power BI REST API Documentation:
https://learn.microsoft.com/en-us/rest/api/power-bi/
