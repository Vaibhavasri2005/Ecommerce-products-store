#!/bin/bash

# Load testing script to simulate multiple concurrent users
# Requires Apache Bench (ab) - install with: apt install apache2-utils

echo "=========================================="
echo "Load Testing E-Commerce Platform"
echo "=========================================="
echo ""

# Configuration
URL="http://localhost"
TOTAL_REQUESTS=1000
CONCURRENT_USERS=50

echo "Test Configuration:"
echo "  Target URL: $URL"
echo "  Total Requests: $TOTAL_REQUESTS"
echo "  Concurrent Users: $CONCURRENT_USERS"
echo ""

# Check if Apache Bench is installed
if ! command -v ab &> /dev/null; then
    echo "Apache Bench (ab) is not installed."
    echo "Install with: sudo apt install apache2-utils"
    exit 1
fi

echo "Starting load test..."
echo ""

# Run load test
ab -n $TOTAL_REQUESTS -c $CONCURRENT_USERS -g results.tsv $URL/ > load_test_results.txt

echo ""
echo "Load test complete!"
echo ""
echo "Results saved to: load_test_results.txt"
echo ""

# Display summary
echo "Summary:"
cat load_test_results.txt | grep -E "(Requests per second|Time per request|Transfer rate|Failed requests)"

echo ""
echo "Check server logs to see load distribution across servers:"
echo "  tail -f /opt/ecommerce/logs/server*-access.log"
