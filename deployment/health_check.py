#!/usr/bin/env python3
"""
Health check script for monitoring application servers
Can be used with monitoring tools or cron jobs
"""

import requests
import sys
import os

SERVERS = [
    {'name': 'Server 1', 'url': 'http://localhost:5001'},
    {'name': 'Server 2', 'url': 'http://localhost:5002'},
    {'name': 'Server 3', 'url': 'http://localhost:5003'},
]

NGINX_URL = 'http://localhost'

def check_server(server):
    """Check if a server is responding"""
    try:
        response = requests.get(f"{server['url']}/", timeout=5)
        if response.status_code == 200:
            return True, "OK"
        else:
            return False, f"HTTP {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Connection refused"
    except requests.exceptions.Timeout:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)

def check_nginx():
    """Check if Nginx load balancer is responding"""
    try:
        response = requests.get(NGINX_URL, timeout=5)
        if response.status_code == 200:
            return True, "OK"
        else:
            return False, f"HTTP {response.status_code}"
    except Exception as e:
        return False, str(e)

def main():
    print("="*50)
    print("E-Commerce Platform Health Check")
    print("="*50)
    print()
    
    all_healthy = True
    
    # Check Nginx
    print("Checking Nginx Load Balancer...")
    nginx_healthy, nginx_status = check_nginx()
    print(f"  Nginx: {'✓' if nginx_healthy else '✗'} {nginx_status}")
    if not nginx_healthy:
        all_healthy = False
    print()
    
    # Check individual servers
    print("Checking Application Servers...")
    for server in SERVERS:
        healthy, status = check_server(server)
        print(f"  {server['name']}: {'✓' if healthy else '✗'} {status}")
        if not healthy:
            all_healthy = False
    
    print()
    print("="*50)
    
    if all_healthy:
        print("Status: All systems operational")
        return 0
    else:
        print("Status: Some services are down")
        return 1

if __name__ == '__main__':
    sys.exit(main())
