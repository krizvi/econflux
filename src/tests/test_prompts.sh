#!/bin/bash

ENDPOINT="http://localhost:8080/invocations"

echo "Testing EconFlux Agent with Sophisticated Prompts"
echo "=================================================="
echo ""

# Test prompt 1
echo "🔍 Test 1: Tesla vs Ford momentum analysis"
curl -X POST $ENDPOINT \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Analyze Tesla'\''s price momentum over the past 5 days and compare it against Ford'\''s performance during the same period. Which stock showed stronger relative strength, and what might this indicate about sector rotation dynamics?"}' \
  | jq -r '.result' 2>/dev/null || echo "Failed"

echo -e "\n\n---\n"
sleep 2

# Test prompt 7
echo "🔍 Test 2: Retail peer analysis"
curl -X POST $ENDPOINT \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Conduct a peer analysis of Walmart, Target, and Costco. Compare their price performance, earnings quality, and upcoming catalyst calendars. Which retailer presents the most compelling risk-reward profile right now?"}' \
  | jq -r '.result' 2>/dev/null || echo "Failed"

echo -e "\n\n---\n"
sleep 2

# Test prompt 18
echo "🔍 Test 3: Mega-cap tech leadership"
curl -X POST $ENDPOINT \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Generate a comprehensive view of how the mega-cap tech stocks (Apple, Microsoft, Google, Amazon, Meta) have performed relative to each other this week. Which names are showing leadership, and do their earnings calendars suggest this leadership might persist or reverse?"}' \
  | jq -r '.result' 2>/dev/null || echo "Failed"

echo -e "\n\nTests complete!"