#!/bin/bash
while IFS= read -r line; do
    echo "$line"
    sleep 0.05
done < ~/.splash

IP=$(hostname -I | awk '{print $1}')
BATTERY=$(python3 -c "import json; s=json.load(open('/tmp/battery_status.json')); print(f\"{s['percent']}% \")")
TIMESTAMP=$(date '+%Y.%m.%d  %H:%M:%S')

sleep 0.05
echo ""
sleep 1
echo "       IP: $IP   |   BAT: $BATTERY   |   $TIMESTAMP"
sleep 0.05
echo ""
sleep 0.05
echo ""
sleep 0.05
echo ""
sleep 0.05
echo ""
sleep 1
