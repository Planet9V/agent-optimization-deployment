#!/bin/bash

# Deployment Monitoring Dashboard
# Real-time monitoring of Docker containers and services

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Configuration
REFRESH_INTERVAL=5
HEALTH_ENDPOINTS=(
  "http://localhost:3000/health:Frontend"
  "http://localhost:5000/health:Backend"
  "http://localhost:7474:Neo4j"
)

# Function to clear screen and show header
show_header() {
  clear
  echo -e "${BOLD}${CYAN}╔════════════════════════════════════════════════════════════════════╗${NC}"
  echo -e "${BOLD}${CYAN}║          DEPLOYMENT MONITORING DASHBOARD                          ║${NC}"
  echo -e "${BOLD}${CYAN}║          Last Updated: $(date '+%Y-%m-%d %H:%M:%S')                        ║${NC}"
  echo -e "${BOLD}${CYAN}╚════════════════════════════════════════════════════════════════════╝${NC}"
  echo ""
}

# Function to check container status
check_containers() {
  echo -e "${BOLD}${WHITE}📦 CONTAINER STATUS${NC}"
  echo -e "${CYAN}────────────────────────────────────────────────────────────────────${NC}"

  # Get all containers from docker-compose
  local containers=$(docker-compose ps --services 2>/dev/null)

  if [ -z "$containers" ]; then
    echo -e "${RED}✗ No containers found${NC}"
    echo ""
    return
  fi

  printf "%-20s %-15s %-10s %-15s\n" "CONTAINER" "STATUS" "HEALTH" "UPTIME"
  echo -e "${CYAN}────────────────────────────────────────────────────────────────────${NC}"

  while IFS= read -r container; do
    local status=$(docker-compose ps "$container" 2>/dev/null | grep "$container" | awk '{print $4}')
    local health=$(docker inspect --format='{{.State.Health.Status}}' "$(docker-compose ps -q "$container" 2>/dev/null)" 2>/dev/null || echo "none")
    local uptime=$(docker inspect --format='{{.State.StartedAt}}' "$(docker-compose ps -q "$container" 2>/dev/null)" 2>/dev/null)

    # Calculate uptime duration
    if [ -n "$uptime" ] && [ "$uptime" != "0001-01-01T00:00:00Z" ]; then
      local start_seconds=$(date -d "$uptime" +%s 2>/dev/null)
      local current_seconds=$(date +%s)
      local duration=$((current_seconds - start_seconds))
      local uptime_formatted=$(printf '%dd %dh %dm' $((duration/86400)) $((duration%86400/3600)) $((duration%3600/60)))
    else
      local uptime_formatted="N/A"
    fi

    # Color code status
    if [[ "$status" == *"Up"* ]]; then
      local status_color="${GREEN}●${NC}"
      local status_text="${GREEN}Running${NC}"
    else
      local status_color="${RED}●${NC}"
      local status_text="${RED}Stopped${NC}"
    fi

    # Color code health
    case "$health" in
      "healthy")
        local health_text="${GREEN}Healthy${NC}"
        ;;
      "unhealthy")
        local health_text="${RED}Unhealthy${NC}"
        ;;
      "starting")
        local health_text="${YELLOW}Starting${NC}"
        ;;
      *)
        local health_text="${CYAN}N/A${NC}"
        ;;
    esac

    printf "${status_color} %-18s %-22b %-17b %s\n" "$container" "$status_text" "$health_text" "$uptime_formatted"
  done <<< "$containers"

  echo ""
}

# Function to check health endpoints
check_health_endpoints() {
  echo -e "${BOLD}${WHITE}🏥 HEALTH ENDPOINTS${NC}"
  echo -e "${CYAN}────────────────────────────────────────────────────────────────────${NC}"

  printf "%-40s %-10s %-15s\n" "ENDPOINT" "STATUS" "RESPONSE TIME"
  echo -e "${CYAN}────────────────────────────────────────────────────────────────────${NC}"

  for endpoint_info in "${HEALTH_ENDPOINTS[@]}"; do
    IFS=':' read -r url name <<< "$endpoint_info"

    # Measure response time
    local start=$(date +%s%N)
    local response=$(curl -s -o /dev/null -w "%{http_code}" --max-time 3 "$url" 2>/dev/null)
    local end=$(date +%s%N)
    local duration=$(( (end - start) / 1000000 ))

    if [ "$response" = "200" ] || [ "$response" = "204" ]; then
      local status="${GREEN}✓ OK${NC}"
      local time_text="${duration}ms"
    elif [ -z "$response" ]; then
      local status="${RED}✗ Timeout${NC}"
      local time_text="N/A"
    else
      local status="${YELLOW}! ${response}${NC}"
      local time_text="${duration}ms"
    fi

    printf "%-40s %-17b %s\n" "$name ($url)" "$status" "$time_text"
  done

  echo ""
}

# Function to check resource usage
check_resources() {
  echo -e "${BOLD}${WHITE}💾 RESOURCE USAGE${NC}"
  echo -e "${CYAN}────────────────────────────────────────────────────────────────────${NC}"

  printf "%-20s %-12s %-12s %-15s\n" "CONTAINER" "CPU %" "MEMORY" "NET I/O"
  echo -e "${CYAN}────────────────────────────────────────────────────────────────────${NC}"

  # Get container stats
  docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" 2>/dev/null | tail -n +2 | while read -r line; do
    local name=$(echo "$line" | awk '{print $1}')
    local cpu=$(echo "$line" | awk '{print $2}')
    local mem=$(echo "$line" | awk '{print $3,$4,$5}')
    local net=$(echo "$line" | awk '{print $6,$7}')

    # Color code CPU usage
    local cpu_value=$(echo "$cpu" | sed 's/%//')
    if (( $(echo "$cpu_value > 80" | bc -l 2>/dev/null || echo 0) )); then
      cpu="${RED}${cpu}${NC}"
    elif (( $(echo "$cpu_value > 50" | bc -l 2>/dev/null || echo 0) )); then
      cpu="${YELLOW}${cpu}${NC}"
    else
      cpu="${GREEN}${cpu}${NC}"
    fi

    printf "%-20s %-19b %-12s %s\n" "$name" "$cpu" "$mem" "$net"
  done

  echo ""
}

# Function to show recent logs
show_recent_logs() {
  echo -e "${BOLD}${WHITE}📋 RECENT LOGS (Last 5 lines per service)${NC}"
  echo -e "${CYAN}────────────────────────────────────────────────────────────────────${NC}"

  local containers=$(docker-compose ps --services 2>/dev/null)

  while IFS= read -r container; do
    echo -e "${MAGENTA}▶ $container${NC}"
    docker-compose logs --tail=3 "$container" 2>/dev/null | sed 's/^/  /'
    echo ""
  done <<< "$containers"
}

# Function to check service connectivity
check_connectivity() {
  echo -e "${BOLD}${WHITE}🔗 SERVICE CONNECTIVITY${NC}"
  echo -e "${CYAN}────────────────────────────────────────────────────────────────────${NC}"

  # Check frontend → backend
  local frontend_to_backend=$(docker-compose exec -T frontend curl -s -o /dev/null -w "%{http_code}" http://backend:5000/health 2>/dev/null || echo "000")
  if [ "$frontend_to_backend" = "200" ] || [ "$frontend_to_backend" = "204" ]; then
    echo -e "${GREEN}✓${NC} Frontend → Backend: ${GREEN}Connected${NC}"
  else
    echo -e "${RED}✗${NC} Frontend → Backend: ${RED}Failed (HTTP $frontend_to_backend)${NC}"
  fi

  # Check backend → neo4j
  local backend_to_neo4j=$(docker-compose exec -T backend nc -z neo4j 7687 2>/dev/null && echo "200" || echo "000")
  if [ "$backend_to_neo4j" = "200" ]; then
    echo -e "${GREEN}✓${NC} Backend → Neo4j: ${GREEN}Connected${NC}"
  else
    echo -e "${RED}✗${NC} Backend → Neo4j: ${RED}Failed${NC}"
  fi

  # Check host access
  echo -e "${GREEN}✓${NC} Host → Frontend: http://localhost:3000"
  echo -e "${GREEN}✓${NC} Host → Backend: http://localhost:5000"
  echo -e "${GREEN}✓${NC} Host → Neo4j Browser: http://localhost:7474"

  echo ""
}

# Function to show system info
show_system_info() {
  echo -e "${BOLD}${WHITE}🖥️  SYSTEM INFORMATION${NC}"
  echo -e "${CYAN}────────────────────────────────────────────────────────────────────${NC}"

  # Docker version
  local docker_version=$(docker --version 2>/dev/null | awk '{print $3}' | sed 's/,//')
  echo -e "Docker Version: ${CYAN}$docker_version${NC}"

  # Docker Compose version
  local compose_version=$(docker-compose --version 2>/dev/null | awk '{print $3}' | sed 's/,//')
  echo -e "Docker Compose: ${CYAN}$compose_version${NC}"

  # System load
  local load=$(uptime | awk -F'load average:' '{print $2}')
  echo -e "System Load: ${CYAN}$load${NC}"

  # Disk usage
  local disk=$(df -h . | tail -1 | awk '{print $5}')
  echo -e "Disk Usage: ${CYAN}$disk${NC}"

  echo ""
}

# Function to show footer with controls
show_footer() {
  echo -e "${CYAN}────────────────────────────────────────────────────────────────────${NC}"
  echo -e "${WHITE}Press ${BOLD}Ctrl+C${NC}${WHITE} to exit | Auto-refresh every ${REFRESH_INTERVAL}s${NC}"
  echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
}

# Main monitoring loop
monitor() {
  while true; do
    show_header
    check_containers
    check_health_endpoints
    check_resources
    check_connectivity
    show_system_info
    show_recent_logs
    show_footer

    sleep "$REFRESH_INTERVAL"
  done
}

# Trap Ctrl+C to exit cleanly
trap 'echo -e "\n${GREEN}Monitoring stopped.${NC}"; exit 0' INT

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
  echo -e "${RED}Error: docker-compose is not installed${NC}"
  exit 1
fi

# Check if docker is running
if ! docker info &> /dev/null; then
  echo -e "${RED}Error: Docker is not running${NC}"
  exit 1
fi

# Start monitoring
echo -e "${GREEN}Starting deployment monitoring...${NC}"
sleep 1
monitor
