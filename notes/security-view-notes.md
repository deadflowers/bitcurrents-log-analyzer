### notes and fixes on security function
where IPs have 1-3 hits and the log total is about 240, 200 hits are from 1 offending ip that is throwing off and dramatically changing the charts to be less useful. the block function should recalculate the general view, graph and remove that ip from the results. maybe an option to hide that
differentiate between malicious bot use and normal search spiders vs people

next is security flag triggers in the suspicious_paths.txt file should be categories that are checkboxes on the html doc (all checked by default) and will be in a json file that ships filled out as follows:
```JSON
{
  "http_methods": {
    "description": "Suspicious HTTP verbs often used in scanning or exploitation attempts.",
    "patterns": [
      "^(HEAD|PUT|DELETE|OPTIONS|TRACE|CONNECT) "
    ]
  },
  "webshells": {
    "description": "Common webshell and dropper filenames attackers try to upload or call directly.",
    "patterns": [
      "/w(uwu|c|s|shell|slee)\\.php$",
      "/x(w|w1|s|shell)\\.php$",
      "/qq\\.php$",
      "/ak47\\.php$",
      "/phpstudy\\.php$",
      "/system\\.php$",
      "/cmd\\.php$",
      "/conflg\\.php$",
      "/db(init|_session\\.init|__\\.init)?\\.php$",
      "/mx\\.php$",
      "/lindex\\.php$",
      "/zuoshou\\.php$",
      "/hm\\.php$",
      "/sheep\\.php$",
      "/defect\\.php$",
      "/webslee\\.php$",
      "/qaq?\\.php$",
      "/xshell\\.php$",
      "/wshell\\.php$"
    ]
  },
  "wordpress": {
    "description": "WordPress brute force and exploit probes.",
    "patterns": [
      "/wp-login\\.php",
      "/wp-admin(.*)\\.php",
      "/wp-admin/wp\\.php",
      "/wp-admin/wp-admins\\.php",
      "/wp-admin/network/network\\.php",
      "/wp-admin/maint/about\\.php",
      "/wp-admin/mah\\.php",
      "/wp-admin/js/widgets/(index|cloud)\\.php",
      "/wp-admin/js/index\\.php",
      "/xmlrpc\\.php",
      "/wp-content/uploads/.*\\.php",
      "/wp-includes/.*\\.php"
    ]
  },
  "config_exposure": {
    "description": "Direct requests for secrets, environment files, or version control metadata.",
    "patterns": [
      "/\\.env",
      "/\\.git",
      "/\\.git/config",
      "/\\.svn",
      "/\\.hg",
      "/\\.DS_Store",
      "/\\.htaccess",
      "/\\.htpasswd",
      "/\\.ssh",
      "/\\.aws",
      "/\\.docker",
      "/\\.vscode",
      "/\\.idea",
      "/\\.secrets",
      "/\\.passwords",
      "/\\.gitconfig"
    ]
  },
  "known_exploits": {
    "description": "Paths associated with known vulnerabilities in frameworks and admin consoles.",
    "patterns": [
      "/vendor/phpunit",
      "/solr/admin",
      "/hudson",
      "/manager/html",
      "/HNAP1",
      "/boaform/admin/formLogin",
      "/CFIDE/administrator",
      "/remote/fgt_lang",
      "/owa/auth/logon\\.aspx",
      "/mifs/.*/formLogin\\.html"
    ]
  },
  "webdav": {
    "description": "Probes for WebDAV endpoints and methods.",
    "patterns": [
      "/webdav",
      "PROPFIND "
    ]
  }
}
```

This is being put back together from scraps after my house was robbed by corrupt law officials seeking to hide evidence and anything electronic is missing. that said i do recall a few go arounds on the security flags with thebad actors probing disproportionately and throwing off metrics and even just the aesthetic vibe. but also, we were firing off security flags too loose and well know soon if that is this file or not
