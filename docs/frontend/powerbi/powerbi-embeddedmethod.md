## 📌 Method: Publish to Web (Public Embedding)

### Overview
Will be using a Publish to Web because it is a free, no-authentication-required method that generates an `iframe` you can embed into any website or web application with HTML.

>please note; Not secure. Use only with test data or for non-sensitive public reports.

## Step-by-Step Instructions

### 1. Create and Publish a Power BI Report
- Use **Power BI Desktop** to create a report using sample/test data.
- Click `File > Publish > Publish to Power BI`.
- Select `My Workspace`.

### 2. Generate Embed Code
- Go to [https://app.powerbi.com](https://app.powerbi.com)
- Open your report in the workspace.
- Click `File > Embed report > Publish to web (public)`
- Confirm and copy the iframe code or public URL.

### 3. Embed in Web Application

#### Plain HTML Example:

```html
<iframe 
  width="800" 
  height="600" 
  src="https://app.powerbi.com/view?r=eyJrIjoi...&embed=true" 
  frameborder="0" 
  allowFullScreen="true">
</iframe>
```
#### React Example:
```
const PowerBIEmbed = () => (
  <iframe
    title="Power BI Report"
    width="100%"
    height="600"
    src="https://app.powerbi.com/view?r=eyJrIjoi...&embed=true"
    frameBorder="0"
    allowFullScreen
  />
);
```

#### References

Microsoft Docs:

    Publish to Web in Power BI: https://learn.microsoft.com/power-bi/collaborate-share/service-publish-to-web

    Power BI Desktop: https://powerbi.microsoft.com/desktop

