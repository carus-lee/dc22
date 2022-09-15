echo "----------------------------------"
ps -ef | grep -e prisma.py -e bind_ip -e meteor
echo "----------------------------------"

ps -ef | grep -e prisma.py -e bind_ip -e meteor | awk '{print $2}' | xargs kill -9

echo "=================================="
ps -ef | grep -e prisma.py -e bind_ip -e meteor
echo "=================================="