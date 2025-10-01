    # BitCurrents Log Analyzer

![BitCurrents Logo Placeholder](https://github.com/user-attachments/assets/913d2b11-a09d-4889-bd63-cd8bc6588bbe)

**A powerful, real-time Nginx log analyzer with a focus on security intelligence, performance monitoring, and beautiful data visualization. Powered by the IP2Location API.**

BitCurrents turns raw Nginx logs into actionable insights. It moves beyond simple IP lookups to provide a rich, interactive dashboard that helps you understand your traffic, identify security threats, and diagnose server errors instantly. It's a lightweight, single-page web application built with a Python/Flask backend and a dynamic JavaScript frontend.

---

### 🏆 Built for the IP2Location Programming Contest

This project leverages the power and precision of the **[IP2Location.io](https://www.ip2location.io/)** API to deliver advanced security features, including:
-   **High-Fidelity Geolocation:** Pinpointing the source of traffic with country, city, and ISP data.
-   **Intelligent Bot Detection:** Moving beyond simple user-agent strings.
-   **Bot Impersonator Flagging:** A critical security feature that verifies if traffic claiming to be from major crawlers (like Googlebot) is actually coming from their published IP ranges.

---

## 🔥 Key Features

### 1. Multi-Mode Analysis Dashboard
Switch between three distinct analysis modes, each with a purpose-built dashboard:

#### ✨ General Mode
Your command center for at-a-glance traffic overview.
-   **Rich KPI Cards:** Total Hits, Unique IPs, and critical counts of Impersonator and Suspicious traffic.
-   **Comprehensive Charting:**
    -   Traffic Breakdown (Human, Bots, Crawlers)
    -   Device Types (Desktop, Mobile)
    -   OS & Browser Distribution
    -   HTTP Status Code Distribution
    -   Top Countries & Top Successful Pages
-   **Powerful Filtering:** Instantly hide noisy IPs to see the real signal, and switch between analyzing Unique IPs vs. All Hits.

*![Screenshot of Main Dash Panel][https://github.com/user-attachments/assets/4ba40fe1-6f05-43da-90cb-b49c65e52231 />
)*

#### 🛡️ Security Mode
Proactively hunt for threats and analyze attack patterns.
-   **Dynamic Threat Categories:** Filter logs for specific attack vectors like Config Exposure, Webshells, and WordPress probes using a configurable `security_patterns.json`.
-   **Targeted Visualizations:** See charts for Top Attack Categories and Top Attacking IPs.
-   **Bot Impersonator Detection:** Automatically flags traffic pretending to be a legitimate crawler from an unverified IP address.

*![Screenshot of Security Dash Panel](<img width="1513" height="873" alt="image" src="https://github.com/user-attachments/assets/2ea5ce38-a3cb-4480-9cbe-16b3a497a04e" />
)*

#### 🚨 Error Mode
Quickly diagnose and understand server problems.
-   **Smart Error Parsing:** Intelligently categorizes common Nginx `error.log` messages (e.g., "Backend Unreachable," "Index Forbidden").
-   **Insightful Charts:** Visualize error types and severity levels to prioritize fixes.
-   **In-App Quick Guide:** A helpful "Error Log Tips" modal provides context and troubleshooting advice for common Nginx errors.

*![Screenshot of the Error Mode Dashboard](https://via.placeholder.com/1200x600.png?text=Screenshot:+Error+Dashboard+View)*

### Set Up: 
Clone or download this repository making sure you have app.py, index.html, .env, bots_database.json, suspicious_paths.json are all in the same directory.

*   **Install pyenv:** If you don't have it, follow the installation guide. For macOS/Linux with Homebrew, it looks like this:
    
        `brew install pyenv`
    
    Make sure to follow the post-install instructions to add pyenv init to your shell's startup script (.zshrc, .profile, .bashrc, etc.).
    
*   **Install a Python Version:** Let's use a recent, stable version.
    
        `pyenv install 3.13.0`
      
*   **Create Your Project:**
    
        `mkdir bitcurrents-log-analyzer`
    
        `cd bitcurrents-log-analyzer`
      
*   **Set the Local Python Version:** This command creates a .python-version file in your directory, so pyenv automatically uses this version whenever you're in this folder.
    
        `pyenv local 3.11.5`
      
*   **Create & Activate a Virtual Environment:** This is a best practice within your pyenv version to keep packages project-specific.
    
        `# Create the virtual environment folder named
    '.venv' python -m venv .venv  # Activate it source .venv/bin/activate # Your terminal prompt should now show (.venv)`
      
*   **Create requirements.txt:** This file lists all the Python packages your project needs.  
    Create a file named requirements.txt and add the following:
        
        ```Flask
           flask-cors
           python-dotenv
           requests
        ```
      
*   **Install Dependencies:**
    
        `pip install -r requirements.txt`
      
*   **Set Up API Key:**
    
    *   Sign up for a free account at [IP2Location.io](https://ip2location.io) to get an API key. The free plan is quite capable.
        
    *   Create a file named .env in your project directory and add your key:
           
        `IP2LOCATION_API_KEY=your_actual_api_key_here`

*   **Set Up Environment:** Follow all the steps in "Step 1: Environment Setup with pyenv". Make sure your .venv is activated.
    
*   **Start the Backend:** In your terminal, inside the bitcurrents-log-analyzer directory, run:
        
        `# Make sure you see (.venv) in your prompt python app.py`
        
    The server will start on http://127.0.0.1:5001.
    
*   **Open the Frontend:**
  
Open your terminal in the project directory and activate your pyenv virtual environment:

`source .venv/bin/activate`

### Start Backend: Run the Python server:
```bash
python app.py
```
### Launch Frontend: 
Open index.html in your web browser as `file:///` path

### Analyze:
The dashboard will load with the new dark theme.

- Enter the directory where your logs are stored or copied to.
- Optionally, enter a path fragment to track in the "Track Custom Path"
- Click the "Analyze Logs" button.

The charts will populate, and the detailed IP table will appear below. You can now distinguish OS/Bot and any suspicious paths hit directly in the table.
- Add new paths to your watchlist on-the-fly using the "Add to Suspicious List" feature.

Being conservative wiwth credits we keep an ip cache file as well automatically.

### NGINX 

To display the referrer in Nginx access logs, ensure your `log_format` configuration includes the `$http_referer` variable.

I have in my `nginx.conf` the following:
```
# Logging
    log_format custom_format '$remote_addr - $remote_user [$time_local] '
                          '"$request" $status $body_bytes_sent '
                          '"$http_referer" "$http_user_agent"';
    access_log		      /var/log/nginx/access.log custom_format;
    error_log              /var/log/nginx/error.log warn;
```

Then in my domain conf:
```
# logging
    access_log              /var/log/nginx/site.com.access.log custom_format buffer=512k flush=1m;
    error_log               /var/log/nginx/site.com.error.log warn;
```

Reload
```
sudo systemctl reload nginx
```

** note this app is being pieced back together last minute from memory and snippets in email as the equipment was all taken in a robbery. This project should be in working order if not it's final incarnaton by end of day today or tomorrow latest. and have more complete notes submitted **
