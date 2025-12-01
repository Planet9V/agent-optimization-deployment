
# Stanford STORM: An AI-Powered Knowledge Curation System

Stanford STORM (Structured Task-Oriented Research Machine) is a sophisticated large language model (LLM) system being developed by the Stanford Open Virtual Assistant Lab (OVAL) team1. This advanced technology allows for the creation of high-quality, Wikipedia-style articles from scratch, revolutionizing how knowledge is curated and content is generated1. STORM is a research prototype that supports interactive knowledge curation3. It acts as a research assistant, automatically researching a topic, organizing the information, and generating a full-length report with citations2.

## Key Features and Benefits

Before diving into the complexities of how STORM operates, it's important to understand the key features and benefits this system offers:

- Automated Research: STORM automates the often tedious research process, saving users significant time and effort.
    
- Comprehensive Coverage: By gathering information from a variety of sources, STORM ensures a comprehensive and multifaceted understanding of the topic.
    
- Structured Output: The system generates well-structured articles that resemble Wikipedia entries, with clear headings, subheadings, and proper citations.
    
- Interactive Knowledge Curation: Co-STORM, an extension of STORM, allows for human-AI collaboration, enabling users to actively participate in the research and writing process.
    
- Modularity and Flexibility: STORM supports the customization of language models and retrieval modules, allowing users to tailor the system to their specific needs and preferences.
    

## How STORM Works

STORM employs a unique approach to knowledge curation, utilizing a multi-agent system that simulates a team of experts collaborating on a research project1. This process is divided into two primary stages: pre-writing and writing2.

### Pre-writing Stage

The pre-writing stage focuses on gathering and organizing information. This stage involves the following steps:

  

|Step|Description|
|---|---|
|Knowledge Curation|STORM utilizes various retrieval modules to collect a broad range of information on the given topic from sources like Wikipedia and You.com2.|
|Outline Generation|STORM analyzes the collected information and generates a hierarchical outline to organize the curated knowledge2. This outline serves as a blueprint for the article, ensuring comprehensive coverage of the subject matter1.|
|Perspective-Guided Question Asking|To improve the depth and breadth of its research, STORM surveys existing articles on similar topics to identify different perspectives2. These perspectives guide the question-asking process, enabling STORM to delve deeper into the subject matter.|
|Simulated Conversation|STORM simulates a conversation between a Wikipedia writer and a topic expert grounded in internet sources2. This simulated conversation allows the language model to update its understanding of the topic and ask follow-up questions, further enhancing the research process.|

### Writing Stage

Once STORM has gathered sufficient information and structured it into an outline, it proceeds to the writing stage to generate the article. This stage involves the following steps:

  

|Step|Description|
|---|---|
|Article Generation|STORM populates the outline with the curated information, generating the main body of the article2. It's important to note that STORM automatically generates citations throughout the article to support factual claims, linking back to the original sources2. This feature is crucial for academic and research writing, as it enhances the credibility and trustworthiness of the generated articles while saving users time and effort compared to manual citation management1.|
|Article Polishing|STORM refines and enhances the written article for better presentation, ensuring clarity, coherence, and readability2.|

## CO-STORM: Collaborative Knowledge Curation

Co-STORM builds upon the foundation of STORM by introducing a collaborative discourse protocol. This protocol facilitates a seamless interaction between humans and AI agents during the knowledge curation process5. Co-STORM includes several key enhancements:

- Moderator Agent: This agent guides the conversation by generating insightful questions and directing attention to areas that require further exploration6.
    
- Human Engagement: Co-STORM allows users to actively participate in the conversation by injecting their own utterances, fostering a truly interactive and collaborative experience6.
    
- Dynamic Mind Map: A dynamic mind map is used to structure the retrieved information into a concept-oriented hierarchy6. This creates a shared conceptual space for both the user and the system, presented in a graphical user interface (GUI) for easy navigation and exploration of the knowledge curation process.
    
- Graphical UI Update: Co-STORM features an updated GUI that provides a user-friendly interface for interacting with the system6.
    

## Implementation and Guidance

To implement and run STORM, follow these steps:

1. Clone the Repository: Clone the STORM repository from GitHub: git clone https://github.com/stanford-oval/storm 2
    
2. Install Dependencies: Install the necessary dependencies using pip install -r requirements.txt7.
    
3. Configure API Keys: Obtain API keys for the desired language models (e.g., OpenAI, Claude) and configure them in the secrets.toml file7. STORM supports a variety of language model families and clients, including GPT, Claude, VLLM, TGI, and Together6. This flexibility allows users to leverage different language models based on their specific needs and preferences.
    
4. Run STORM: Execute the Python script run_storm_wiki_gpt.py for GPT models or run_storm_wiki_claude.py for Claude models4. You can also use run_storm_wiki_mistral.py to run STORM with Mistral-7B-Instruct-v0.2 using a VLLM server4.
    
5. Customize Retriever Module: STORM allows for customization of the Retriever module to integrate different information sources6. For more detailed instructions on customizing the Retriever module, please consult the project documentation on GitHub.
    
6. Run with Your Own Corpus: You can run STORM with your own corpus by creating a CSV file with the following columns: content, title, url, and description4. Ensure each document has a unique URL4.
    

## Running STORM with Mistral

To run STORM with the Mistral-7B-Instruct-v0.2 model using a VLLM server, follow these additional steps:

1. Install VLLM: Install the VLLM library using pip install vllm==0.2.77.
    
2. Launch VLLM Server: Launch the VLLM server with the Mistral model: python -m vllm.entrypoints.openai.api_server --port 6006 --model 'mistralai/Mistral-7B-Instruct-v0.2' 7
    
3. Run STORM: Execute the following command in a terminal window: python examples/run_storm_wiki_mistral.py --url "http://localhost" --port 6006 --output-dir '/notebooks/results/' --do-research --do-generate-outline --do-generate-article --do-polish-article 7
    

## Related Projects by Stanford OVAL

The Stanford OVAL team is engaged in a variety of research projects aimed at developing AI-augmented cognition systems. Here are a few notable examples:

- Noora: An AI-driven platform designed to help individuals with Autism Spectrum Disorder (ASD) improve their social communication skills through specialized exercises8.
    
- WikiChat: An LLM-based chatbot that grounds its responses in Wikipedia to ensure factual accuracy and reduce hallucinations9.
    
- Spinach Agent: A question-answering system that mimics how human experts would write SPARQL queries for Wikidata9.
    
- YelpBot (SUQL): A chatbot that utilizes SUQL (Structured and Unstructured Query Language) to search for restaurants based on both structured data and free-text reviews9.
    

These projects showcase the breadth and depth of OVAL's research in leveraging AI to enhance human cognition and communication.

## Terms of Service

It's important to be aware of the terms of service for using STORM, as outlined on the project's website3. STORM is a research preview and, as such, has limitations and safety measures in place. Users should be aware that:

- STORM may generate offensive content due to limited safety measures.
    
- It should not be used for any illegal, harmful, violent, racist, or sexual purposes.
    
- The generated reports may contain errors, so it's crucial to verify important information.
    
- The generated content does not reflect the developers' viewpoints.
    
- By using STORM, users grant permission to collect their inputs for research purposes and potential distribution under a Creative Commons Attribution (CC-BY) or similar license.
    
- Users should avoid including any personally identifiable information in their inputs.
    

## Synthesis

Stanford STORM is a powerful AI system that automates the research process and generates comprehensive, well-structured articles with citations. Its multi-agent approach, combined with its ability to simulate conversations and incorporate different perspectives, allows it to produce high-quality content that resembles Wikipedia entries. STORM's modularity and flexibility enable users to customize the system to their specific needs, while Co-STORM facilitates human-AI collaboration in the knowledge curation process.

The potential applications of STORM are vast, spanning across education, research, and content creation. As the project continues to evolve, we can expect to see further enhancements and refinements, potentially leading to even more sophisticated and user-friendly knowledge curation tools. The development of STORM and related projects by the Stanford OVAL team signifies a significant step towards harnessing the power of AI to revolutionize how we access, organize, and generate knowledge.

#### Works cited

1. Stanford STORM: Revolutionizing AI-Powered Knowledge Curation | by Cogni Down Under, accessed December 27, 2024, [https://medium.com/@cognidownunder/stanford-storm-revolutionizing-ai-powered-knowledge-curation-35ce51996c19](https://medium.com/@cognidownunder/stanford-storm-revolutionizing-ai-powered-knowledge-curation-35ce51996c19)

2. stanford-oval/storm: An LLM-powered knowledge curation system that researches a topic and generates a full-length report with citations. - GitHub, accessed December 27, 2024, [https://github.com/stanford-oval/storm](https://github.com/stanford-oval/storm)

3. STORM - Stanford University, accessed December 27, 2024, [https://storm.genie.stanford.edu/](https://storm.genie.stanford.edu/)

4. storm/examples/storm_examples/README.md at main · stanford-oval/storm - GitHub, accessed December 27, 2024, [https://github.com/stanford-oval/storm/blob/main/examples/storm_examples/README.md](https://github.com/stanford-oval/storm/blob/main/examples/storm_examples/README.md)

5. storm/README.md at main · stanford-oval/storm - GitHub, accessed December 27, 2024, [https://github.com/stanford-oval/storm/blob/main/README.md](https://github.com/stanford-oval/storm/blob/main/README.md)

6. Releases · stanford-oval/storm - GitHub, accessed December 27, 2024, [https://github.com/stanford-oval/storm/releases](https://github.com/stanford-oval/storm/releases)

7. Running Stanford OVAL's STORM Mistral demo with Paperspace and DSPy, accessed December 27, 2024, [https://blog.paperspace.com/stanford-oval-storm-wikipedia-writer-llm/](https://blog.paperspace.com/stanford-oval-storm-wikipedia-writer-llm/)

8. Stanford OVAL — Projects, accessed December 27, 2024, [https://oval.cs.stanford.edu/projects](https://oval.cs.stanford.edu/projects)

9. Stanford OVAL — Home, accessed December 27, 2024, [https://oval.cs.stanford.edu/](https://oval.cs.stanford.edu/)

**