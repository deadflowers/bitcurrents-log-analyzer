# Bitcurrents Log Analyzer

Web traffic log analyzer featuring IP address insights provided by IP2Location API. Concept is created as a entry for their 2025 Hackathon programming contest.
## BitCurrents Log Analyzer

### Set Up: 
Make sure app.py, index.html, .env, bots_database.json, suspicious_paths.json are all in the same directory.

### Activate Environment: 
Open your terminal in the project directory and activate your pyenv virtual environment:
```bash
source .venv/bin/activate
```
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
