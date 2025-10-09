import re
import os
import json
import sys
import ipaddress
from collections import Counter
from urllib.parse import urlparse
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

# --- Configuration & Loading ---
DEFAULT_LOG_DIR = '.'
IP_CACHE_FILE = 'ip_cache.json'
BOTS_DATABASE_FILE = 'bots_database.json'
SECURITY_PATTERNS_FILE = 'security_patterns.json'
IP2LOCATION_API_KEY = os.getenv('IP2LOCATION_API_KEY')

ACCESS_LOG_REGEX = re.compile(r'(?P<ip>[\d\.]+) - (?P<user>\S+) \[(?P<datetime>[^\]]+)\] "(?P<request_line>.+?)" (?P<status>\d{3}) (?P<size>\d+) "(?P<referrer>[^"]+)" "(?P<user_agent>[^"]+)"')
ERROR_LOG_REGEX = re.compile(r'\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} \[(?P<severity>\w+)\] .*?, client: (?P<ip>[\d\.]+), .*?, (?P<message>.*)')

IP_CACHE, SECURITY_PATTERNS, BOTS_DB, BOT_REGEXES = {}, {}, {}, {}

def load_all_configs():
    global IP_CACHE, SECURITY_PATTERNS, BOTS_DB, BOT_REGEXES
    IP_CACHE = load_json_file(IP_CACHE_FILE)
    SECURITY_PATTERNS = load_json_file(SECURITY_PATTERNS_FILE, is_critical=True)
    BOTS_DB = load_json_file(BOTS_DATABASE_FILE, is_critical=True)
    BOT_REGEXES = {bot_name: re.compile(bot_name, re.IGNORECASE) for bot_name in BOTS_DB}

def load_json_file(filepath, is_critical=False):
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                content = f.read()
                if content: return json.loads(content)
    except (json.JSONDecodeError, IOError) as e:
        print(f"ERROR: Could not read or parse '{filepath}': {e}", file=sys.stderr)
        if is_critical: sys.exit(f"CRITICAL ERROR: App cannot run without '{filepath}'.")
    return {}

ERROR_MAPPING = { "connect() failed": "Backend Unreachable", "directory index of .* is forbidden": "Index Forbidden", "no live upstreams": "All Backends Down", "client intended to send too large body": "Upload Too Large", "worker_connections are not enough": "Resource Limit", "upstream sent too big header": "Buffer Too Small", "upstream timed out": "Backend Timeout" }

def is_ip_in_ranges(ip_str, ranges):
    try:
        ip_addr = ipaddress.ip_address(ip_str)
        for cidr in ranges:
            if ip_addr in ipaddress.ip_network(cidr): return True
    except (ValueError, TypeError): return False
    return False

def classify_ua_and_ip(ua_string, ip):
    if not ua_string or ua_string == '-':
        return {"type": "Human", "name": "Unknown", "os": "Unknown", "browser": "Unknown", "device": "Unknown"}
    ua_lower = ua_string.lower()
    for bot_name, regex in BOT_REGEXES.items():
        if regex.search(ua_string):
            bot_info = BOTS_DB[bot_name]
            bot_type, name = bot_info["type"], bot_name
            if bot_info.get("ips") and bot_info["ips"]:
                if not is_ip_in_ranges(ip, bot_info["ips"]):
                    bot_type, name = "Impersonator", f"{bot_name} (impersonator)"
            return {"type": bot_type, "name": name, "os": "Bot", "browser": "Bot", "device": "Bot"}
    os_name, browser, device = "Unknown", "Unknown", "Desktop"
    if 'android' in ua_lower or 'iphone' in ua_lower: device = "Mobile"
    if 'ipad' in ua_lower: device = "Tablet"
    if 'windows nt' in ua_lower: os_name = "Windows"
    elif 'macintosh' in ua_lower: os_name = "macOS"
    elif 'android' in ua_lower: os_name = "Android"
    elif 'iphone' in ua_lower or 'ipad' in ua_lower: os_name = "iOS"
    elif 'linux' in ua_lower: os_name = "Linux"
    if 'firefox/' in ua_lower: browser = "Firefox"
    elif 'edg/' in ua_lower: browser = "Edge"
    elif 'chrome/' in ua_lower and 'safari/' in ua_lower: browser = "Chrome"
    elif 'safari/' in ua_lower and 'version/' in ua_lower: browser = "Safari"
    return {"type": "Human", "name": "Human", "os": os_name, "browser": browser, "device": device}

def classify_error_message(message):
    for pattern, classification in ERROR_MAPPING.items():
        if re.search(pattern, message): return classification
    return "Other"

def save_json_cache(filepath, data):
    try:
        with open(filepath, 'w') as f: json.dump(data, f, indent=2)
    except IOError as e: print(f"ERROR: Could not write to cache file '{filepath}': {e}", file=sys.stderr)

def get_ip_info(ip):
    if ip in IP_CACHE: return IP_CACHE[ip]
    if not IP2LOCATION_API_KEY: return {"ip": ip, "error": "Missing API Key."}
    try:
        url = f"https://api.ip2location.io/?key={IP2LOCATION_API_KEY}&ip={ip}&format=json"
        response = requests.get(url, timeout=5)
        data = response.json()
        if 'error' in data: raise Exception(data['error']['error_message'])
        IP_CACHE[ip] = {"ip": ip, "country": data.get('country_name'), "city": data.get('city_name'), "isp": data.get('isp'), "raw_data": data}
        save_json_cache(IP_CACHE_FILE, IP_CACHE)
        return IP_CACHE[ip]
    except Exception: return {"ip": ip, "error": "API Lookup Failed", "raw_data": {}}

# Run configuration loading at application startup
load_all_configs()

@app.route('/api/security_patterns', methods=['GET'])
def get_security_patterns(): return jsonify({k: v['description'] for k, v in SECURITY_PATTERNS.items()})

@app.route('/api/log_files', methods=['GET'])
def list_log_files():
    log_dir = request.args.get('log_dir', '').strip() or DEFAULT_LOG_DIR
    if not os.path.isdir(log_dir): return jsonify({"error": f"Directory not found: '{log_dir}'"}), 404
    try:
        files = [f for f in os.listdir(log_dir) if f.endswith('.log') or 'log' in f]
        return jsonify(sorted(files))
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route('/api/analyze', methods=['GET'])
def analyze_logs():
    mode, limit = request.args.get('mode', 'general'), int(request.args.get('limit', 50))
    log_dir = request.args.get('log_dir', '').strip() or DEFAULT_LOG_DIR
    selected_files = request.args.get('files', '').split(',')
    if not selected_files or not selected_files[0]: return jsonify({"error": "No log files selected."}), 400
    all_lines = []
    for file_name in selected_files:
        try:
            with open(os.path.join(log_dir, file_name), 'r', errors='ignore') as f: all_lines.extend(f.readlines())
        except IOError: return jsonify({"error": f"Could not read file: {file_name}"}), 404
    if mode == "error": results = process_error_logs(all_lines, limit)
    else: results = process_access_logs(all_lines, mode, request.args.get('sec_cats', '').split(','), limit)
    return jsonify({"results": results})

def process_access_logs(lines, mode, sec_cats, limit):
    all_requests_with_class = []
    for line in lines:
        match = ACCESS_LOG_REGEX.match(line)
        if not match: continue
        entry = match.groupdict()
        classification = classify_ua_and_ip(entry['user_agent'], entry['ip'])
        violation_category = None
        if SECURITY_PATTERNS:
            for cat, details in SECURITY_PATTERNS.items():
                for pattern in details['patterns']:
                    if re.search(pattern, entry['request_line'], re.IGNORECASE):
                        violation_category = cat; break
                if violation_category: break
        if classification['type'] == 'Human' and violation_category:
            classification['type'] = 'Suspicious Activity'
        if mode == 'security' and (not violation_category or (sec_cats and violation_category not in sec_cats)):
            continue
        all_requests_with_class.append({**entry, "classification": classification, "violation": violation_category})

    ip_data, processed_ips = {}, set()
    for entry in reversed(all_requests_with_class):
        ip = entry['ip']
        if len(processed_ips) >= limit and ip not in processed_ips: continue
        if ip not in ip_data:
            ip_data[ip] = { "geo": get_ip_info(ip), "requests": [] }
        ip_data[ip]['requests'].append(entry)
        processed_ips.add(ip)
            
    results = [{"ip": ip, **d['geo'], "requests": d['requests']} for ip, d in ip_data.items()]
    return results
    
def process_error_logs(lines, limit):
    ip_data, processed_ips = {}, set()
    for line in reversed(lines):
        match = ERROR_LOG_REGEX.search(line)
        if not match: continue
        ip = match.group('ip')
        if len(processed_ips) >= limit and ip not in processed_ips: continue
        entry = match.groupdict()
        if ip not in ip_data: ip_data[ip] = {"geo": get_ip_info(ip), "errors": []}
        entry['classification'] = classify_error_message(entry['message'])
        ip_data[ip]['errors'].append(entry)
        processed_ips.add(ip)
    results = [{"ip": ip, **d['geo'], "errors": d['errors']} for ip, d in ip_data.items()]
    return results

if __name__ == '__main__':
    app.run(debug=True, port=5001)
