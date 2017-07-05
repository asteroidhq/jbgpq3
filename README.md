# jbgpq3
A HTTP/JSON wrapper for bgpq3 with simple caching.  This tool returns RADB data in a JSON format and provides a little bit of cacheing.  It is useful if you want to provide access to RPSL data to development teams in a simple JSON format.

# Requirements
Python, Flask, and the bgpq3 binary installed on the local machine.

# Usage:
Call /prefix/[as-set] or /prefix/AS[as-number] and you will get some JSON to consume
```
tatou:sputnik andy$ curl http://localhost:5010/prefix/as44504
{
  "as_set": "as44504", 
  "cache_age_seconds": 0, 
  "cache_hit": false, 
  "prefixes_ipv4": [
    {
      "exact": true, 
      "prefix": "91.194.68.0/24"
    }
  ], 
  "prefixes_ipv6": []
}
```