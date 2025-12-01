#!/bin/bash
# Level 5 Deployment Helper Script
# AEON Digital Twin - Information Streams Layer

echo "================================================"
echo "AEON DIGITAL TWIN - LEVEL 5 DEPLOYMENT"
echo "Information Streams Layer (6,000 nodes)"
echo "================================================"
echo ""

# Configuration
SCRIPTS_DIR="/home/jim/2_OXOT_Projects_Dev/scripts"
TESTS_DIR="/home/jim/2_OXOT_Projects_Dev/tests"
DATA_DIR="/home/jim/2_OXOT_Projects_Dev/data"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if Neo4j is running
check_neo4j() {
    echo "Checking Neo4j status..."
    if systemctl is-active --quiet neo4j; then
        echo -e "${GREEN}✓ Neo4j is running${NC}"
        return 0
    else
        echo -e "${RED}✗ Neo4j is not running${NC}"
        echo "Please start Neo4j with: sudo systemctl start neo4j"
        return 1
    fi
}

# Function to display menu
show_menu() {
    echo ""
    echo "DEPLOYMENT OPTIONS:"
    echo "==================="
    echo "1) Generate Level 5 data (5,543 nodes)"
    echo "2) Deploy test dataset (11 nodes)"
    echo "3) Deploy full dataset (5,543 nodes)"
    echo "4) Run integration tests"
    echo "5) View deployment report"
    echo "6) Full deployment (all steps)"
    echo "7) Exit"
    echo ""
}

# Function to generate data
generate_data() {
    echo -e "${YELLOW}Generating Level 5 data...${NC}"
    cd "$SCRIPTS_DIR"
    python3 level5_data_generator.py

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Data generation complete${NC}"
        echo "  Generated file: $DATA_DIR/level5_generated_data.json"

        # Generate Cypher scripts
        echo -e "${YELLOW}Converting to Cypher...${NC}"
        python3 level5_cypher_converter.py

        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ Cypher scripts generated${NC}"
            echo "  Main script: $SCRIPTS_DIR/level5_deployment.cypher"
            echo "  Test script: $SCRIPTS_DIR/level5_test.cypher"
        fi
    else
        echo -e "${RED}✗ Data generation failed${NC}"
        return 1
    fi
}

# Function to deploy test dataset
deploy_test() {
    echo -e "${YELLOW}Deploying test dataset (11 nodes)...${NC}"

    # Prompt for credentials
    read -p "Neo4j username [neo4j]: " NEO4J_USER
    NEO4J_USER=${NEO4J_USER:-neo4j}

    read -s -p "Neo4j password: " NEO4J_PASSWORD
    echo ""

    cd "$SCRIPTS_DIR"

    # Try using cypher-shell
    if command -v cypher-shell &> /dev/null; then
        echo "Using cypher-shell..."
        cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" < level5_test.cypher

        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ Test deployment complete${NC}"
        else
            echo -e "${RED}✗ Test deployment failed${NC}"
            echo "Check credentials and try again"
        fi
    else
        echo -e "${YELLOW}cypher-shell not found. Copy the following to Neo4j Browser:${NC}"
        echo "----------------------------------------"
        head -50 level5_test.cypher
        echo "----------------------------------------"
        echo "Full file: $SCRIPTS_DIR/level5_test.cypher"
    fi
}

# Function to deploy full dataset
deploy_full() {
    echo -e "${YELLOW}Deploying full dataset (5,543 nodes)...${NC}"
    echo -e "${YELLOW}This will create approximately 16,000 relationships${NC}"

    read -p "Continue? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Deployment cancelled"
        return 1
    fi

    # Prompt for credentials
    read -p "Neo4j username [neo4j]: " NEO4J_USER
    NEO4J_USER=${NEO4J_USER:-neo4j}

    read -s -p "Neo4j password: " NEO4J_PASSWORD
    echo ""

    cd "$SCRIPTS_DIR"

    # Try Python deployer first
    echo "Attempting Python deployment..."
    export NEO4J_URI='bolt://localhost:7687'
    export NEO4J_USER
    export NEO4J_PASSWORD

    python3 level5_neo4j_deployer.py

    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}Python deployment failed. Trying cypher-shell...${NC}"

        if command -v cypher-shell &> /dev/null; then
            cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" < level5_deployment.cypher

            if [ $? -eq 0 ]; then
                echo -e "${GREEN}✓ Full deployment complete${NC}"
            else
                echo -e "${RED}✗ Deployment failed${NC}"
            fi
        else
            echo -e "${YELLOW}Manual deployment required:${NC}"
            echo "1. Open Neo4j Browser"
            echo "2. Copy contents of: $SCRIPTS_DIR/level5_deployment.cypher"
            echo "3. Execute in batches of 100 statements"
        fi
    else
        echo -e "${GREEN}✓ Full deployment complete${NC}"
    fi
}

# Function to run integration tests
run_tests() {
    echo -e "${YELLOW}Running integration tests...${NC}"

    read -p "Neo4j username [neo4j]: " NEO4J_USER
    NEO4J_USER=${NEO4J_USER:-neo4j}

    read -s -p "Neo4j password: " NEO4J_PASSWORD
    echo ""

    cd "$TESTS_DIR"

    if command -v cypher-shell &> /dev/null; then
        cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASSWORD" < level5_integration_tests.cypher

        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ Integration tests complete${NC}"
        else
            echo -e "${RED}✗ Integration tests failed${NC}"
        fi
    else
        echo -e "${YELLOW}cypher-shell not found${NC}"
        echo "Test file location: $TESTS_DIR/level5_integration_tests.cypher"
        echo "Run manually in Neo4j Browser"
    fi
}

# Function to view report
view_report() {
    REPORT_FILE="/home/jim/2_OXOT_Projects_Dev/reports/LEVEL5_DEPLOYMENT_COMPLETION_REPORT.md"

    if [ -f "$REPORT_FILE" ]; then
        less "$REPORT_FILE"
    else
        echo -e "${RED}Report not found: $REPORT_FILE${NC}"
    fi
}

# Function for full deployment
full_deployment() {
    echo -e "${GREEN}Starting full Level 5 deployment process...${NC}"

    # Step 1: Generate data
    generate_data
    if [ $? -ne 0 ]; then
        echo -e "${RED}Stopping due to data generation failure${NC}"
        return 1
    fi

    echo ""
    sleep 2

    # Step 2: Deploy test dataset
    echo "Testing with small dataset first..."
    deploy_test

    echo ""
    read -p "Test deployment successful? Continue with full deployment? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Full deployment cancelled"
        return 1
    fi

    # Step 3: Deploy full dataset
    deploy_full

    echo ""
    sleep 2

    # Step 4: Run tests
    echo "Running validation tests..."
    run_tests

    echo ""
    echo -e "${GREEN}================================================${NC}"
    echo -e "${GREEN}LEVEL 5 DEPLOYMENT PROCESS COMPLETE${NC}"
    echo -e "${GREEN}================================================${NC}"
    echo ""
    echo "Summary:"
    echo "  - 5,543 nodes generated"
    echo "  - 5,698 Cypher statements created"
    echo "  - Deployment scripts ready"
    echo "  - Integration tests prepared"
    echo ""
    echo "View full report: $REPORT_FILE"
}

# Main script logic
echo "Checking prerequisites..."

# Check if Neo4j is running
check_neo4j
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Warning: Neo4j appears to be offline${NC}"
    echo "Some operations may fail without Neo4j running"
fi

# Check Python dependencies
python3 -c "import neo4j" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Installing neo4j Python driver...${NC}"
    pip3 install neo4j
fi

# Main menu loop
while true; do
    show_menu
    read -p "Select option: " choice

    case $choice in
        1)
            generate_data
            ;;
        2)
            deploy_test
            ;;
        3)
            deploy_full
            ;;
        4)
            run_tests
            ;;
        5)
            view_report
            ;;
        6)
            full_deployment
            ;;
        7)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option${NC}"
            ;;
    esac

    echo ""
    read -p "Press Enter to continue..."
done