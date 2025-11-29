#!/bin/bash

ENDPOINT="http://localhost:8080/invocations"

echo "Testing EconFlux with Street-Level Prompts"
echo "=========================================="
echo ""

echo "💬 Test 1: Tesla vs Ford (casual)"
curl -X POST $ENDPOINT \
  -H "Content-Type: application/json" \
  -d '{"prompt": "I keep hearing about Tesla everywhere. How has it been doing lately compared to Ford? Like, which one has been going up more in the past week or so? Does this mean people are switching from old car companies to electric ones?"}' \
  | jq -r '.result' 2>/dev/null || echo "Failed"

echo -e "\n\n---\n"
sleep 2

echo "💬 Test 2: Walmart vs Target vs Costco (shopping angle)"
curl -X POST $ENDPOINT \
  -H "Content-Type: application/json" \
  -d '{"prompt": "I shop at Walmart, Target, and Costco. Which one of these stores is the best stock to own right now? Compare how they'\''ve been doing, when they report earnings, and which looks like the safest bet with good upside."}' \
  | jq -r '.result' 2>/dev/null || echo "Failed"

echo -e "\n\n---\n"
sleep 2

echo "💬 Test 3: FAANG leadership (everyday language)"
curl -X POST $ENDPOINT \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Big tech stocks - Apple, Microsoft, Google, Amazon, Facebook. Which ones are leading the pack this week and which are lagging? Based on when they report earnings, will the winners keep winning or is a rotation coming?"}' \
  | jq -r '.result' 2>/dev/null || echo "Failed"

echo -e "\n\n---\n"
sleep 2


echo "Testing EconFlux Agent with Sophisticated Prompts"
echo "=================================================="
echo ""

echo "🔍 Test 4: Tesla vs Ford momentum analysis"
curl -X POST $ENDPOINT \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Analyze Tesla'\''s price momentum over the past 5 days and compare it against Ford'\''s performance during the same period. Which stock showed stronger relative strength, and what might this indicate about sector rotation dynamics?"}' \
  | jq -r '.result' 2>/dev/null || echo "Failed"

echo -e "\n\n---\n"
sleep 2

echo "🔍 Test 5: Retail peer analysis"
curl -X POST $ENDPOINT \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Conduct a peer analysis of Walmart, Target, and Costco. Compare their price performance, earnings quality, and upcoming catalyst calendars. Which retailer presents the most compelling risk-reward profile right now?"}' \
  | jq -r '.result' 2>/dev/null || echo "Failed"

echo -e "\n\n---\n"
sleep 2

echo "🔍 Test 6: Mega-cap tech leadership"
curl -X POST $ENDPOINT \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Generate a comprehensive view of how the mega-cap tech stocks (Apple, Microsoft, Google, Amazon, Meta) have performed relative to each other this week. Which names are showing leadership, and do their earnings calendars suggest this leadership might persist or reverse?"}' \
  | jq -r '.result' 2>/dev/null || echo "Failed"

echo -e "\n\nTests complete!"