# Research Prompts for Deep Exploration

The following prompts are designed to gather in-depth information on critical aspects of the M&A Due Diligence Code Assessment Automation Platform. Each prompt is structured to elicit comprehensive, actionable information that can be directly applied to the implementation.

## 1. Linux-Native Security Tool Containerization

"Provide a comprehensive guide for containerizing the following Linux-native security assessment tools: Syft, Grype, Semgrep, FindSecBugs, Bandit, ESLint, SonarQube Scanner CLI, ScanCode Toolkit, LicenseFinder, Sigstore, in-toto, YARA, and Capa. For each tool, include:

1. Base Docker image recommendation
2. Installation dependencies and commands
3. Configuration file requirements
4. Command-line usage patterns
5. Output processing approach
6. Volume mapping strategy
7. Resource constraints
8. Common containerization issues and solutions
9. Health check implementation
10. Example Dockerfile and docker-compose definition"

## 2. Finding Normalization and Deduplication Framework

"Design a comprehensive framework for normalizing and deduplicating security findings from multiple assessment tools. The framework should address:

1. Common schema definition for all security findings
2. Severity normalization across different rating systems
3. Location mapping for findings in source code
4. Confidence scoring methodology
5. Finding fingerprinting for deduplication
6. Rule-based and machine learning approaches to deduplication
7. False positive reduction techniques
8. Finding enrichment with contextual information
9. Data storage optimization for quick retrieval
10. Example implementation in Python with pseudocode"

## 3. Vector Database Implementation for Security Findings

"Provide a detailed implementation guide for using a vector database (specifically Qdrant) to store and query security assessment findings. Include:

1. Data modeling for security findings
2. Embedding strategy for different finding types
3. Index configuration for optimal performance
4. Query construction for common use cases
5. Similarity search implementation
6. Integration with AI analysis components
7. Performance optimization techniques
8. Scaling considerations
9. Backup and recovery strategy
10. Example implementation code in Python"

## 4. Multi-Language Security Analysis Strategy

"Develop a comprehensive strategy for security analysis across multiple programming languages (specifically Scala, Node.js, Python, Java, and React). Address:

1. Language detection methodology
2. Language-specific tool selection criteria
3. Custom rule configuration by language
4. Handling of mixed-language repositories
5. Framework and library detection
6. Language-specific vulnerability patterns
7. Optimization for analysis speed by language
8. Output normalization across language tools
9. Language-specific false positive patterns
10. Test repositories for validating language detection and analysis"

## 5. Report Generation and Visualization Framework

"Design a flexible framework for generating security assessment reports and visualizations. Include:

1. Report templating system design
2. Data aggregation strategy for executive summaries
3. Finding categorization and organization methodology
4. Risk scoring and prioritization approach
5. Visualization types for different data aspects
6. Interactive visualization implementation with three.js
7. Export format generation (PDF, HTML, Excel)
8. Customization options for different stakeholders
9. Delta analysis for version comparison
10. Example implementation with code samples"

## 6. Error Handling and Recovery Mechanism

"Create a robust error handling and recovery framework for a security assessment automation platform. Include:

1. Error categorization and classification
2. Retry strategy for transient failures
3. Graceful degradation approach for persistent failures
4. Checkpoint and resume capability for long-running processes
5. Task dependency management during partial failures
6. Error notification and escalation workflow
7. Recovery validation methodology
8. Performance impact minimization
9. Logging and diagnostic information capture
10. Example implementation patterns in Python"

## 7. Docker Resource Optimization for Security Tools

"Provide detailed guidance on optimizing Docker resource allocation for security assessment tools. Address:

1. CPU and memory profiling for each tool
2. Container resource limitation strategy
3. Parallel execution optimization
4. Volume performance considerations
5. Network configuration for tool communication
6. Temporary storage management
7. Cache optimization for repeated analysis
8. Container lifecycle management
9. Resource monitoring and alerting
10. Example Docker Compose configuration with resource settings"

## 8. Integration Testing Framework for Security Analysis Pipeline

"Design a comprehensive testing framework for validating a security analysis pipeline. Include:

1. Test repository characteristics and requirements
2. Known vulnerability seeding methodology
3. Tool output validation approach
4. Integration test suite design
5. Performance benchmark methodology
6. Regression testing strategy
7. Mocking approach for external dependencies
8. CI/CD integration for automated testing
9. Test result reporting and analysis
10. Example test implementation in Python"

## 9. Web Interface Design for Security Assessment Results

"Develop a detailed specification for a web interface to display security assessment results. Include:

1. User journey mapping for different personas
2. Dashboard layout and component design
3. Finding exploration interface design
4. Visualization component specifications
5. Report customization interface
6. Responsive design considerations
7. Accessibility requirements
8. Performance optimization for large result sets
9. Frontend state management approach
10. Example React component architecture"

## 10. AI-Powered Analysis of Security Findings

"Create a framework for AI-powered analysis of security assessment findings. Address:

1. Finding classification and categorization
2. Severity and impact prediction
3. Remediation recommendation generation
4. Pattern recognition across repositories
5. Anomaly detection for unusual vulnerabilities
6. False positive reduction through AI
7. NLP techniques for finding enrichment
8. Vector embedding strategy for findings
9. Query optimization for AI analysis
10. Example implementation approach using modern AI techniques"

## 11. Tool Output Standardization Framework

"Design a framework for standardizing outputs from diverse security assessment tools. Include:

1. Output format analysis for supported tools
2. Parser implementation strategy for different formats
3. Transformer components for normalization
4. Schema validation methodology
5. Error handling for malformed outputs
6. Performance considerations for large outputs
7. Incremental processing for streaming outputs
8. Output enrichment pipeline
9. Storage format optimization
10. Example code for key transformers"

## 12. Repository Language Detection and Tool Selection Strategy

"Develop a detailed strategy for detecting repository languages and selecting appropriate assessment tools. Address:

1. File pattern and extension analysis techniques
2. Advanced language detection approaches beyond extensions
3. Framework and library identification
4. Language proportion calculation and threshold decisions
5. Mixed-language repository handling strategy
6. Tool selection logic based on language makeup
7. Configuration generation for language-specific tools
8. Performance optimization for large repositories
9. Incremental analysis for repository changes
10. Example implementation with decision trees"

## 13. License Compliance Analysis Framework

"Create a comprehensive framework for analyzing license compliance in software repositories. Include:

1. License identification methodology
2. License compatibility analysis
3. Dependency graph construction for license inheritance
4. License obligation extraction and classification
5. Risk scoring for license combinations
6. Remediation guidance generation
7. License policy enforcement
8. Custom license handling
9. Report generation for compliance stakeholders
10. Example implementation with license compatibility matrix"

## 14. SBOM Generation and Utilization Strategy

"Develop a detailed strategy for generating and utilizing Software Bills of Materials (SBOMs) in security assessments. Address:

1. SBOM format selection criteria (CycloneDX vs. SPDX)
2. Tool selection for different repository types
3. SBOM quality validation methodology
4. Integration with vulnerability scanning tools
5. Version management for SBOMs
6. Delta analysis between SBOMs
7. Storage and retrieval optimization
8. SBOM enrichment with additional metadata
9. Executive reporting from SBOM data
10. Example implementation workflow"

## 15. Security Assessment Pipeline Optimization

"Design an optimized pipeline for security assessment of multiple repositories. Include:

1. Task dependency graph construction
2. Parallel execution strategies
3. Resource allocation optimization
4. Caching mechanisms for intermediate results
5. Incremental analysis approach
6. Progress tracking and estimation
7. Pipeline failure handling
8. Performance monitoring and bottleneck identification
9. Configuration-driven pipeline customization
10. Example implementation with task orchestration"