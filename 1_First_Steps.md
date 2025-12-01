To get OpenSPG fully running locally in October 2025, after completing the model configuration you mentioned, you need to complete four main setup stages: starting the core services, creating a knowledge project, loading data, and enabling reasoning/query execution. The following reflects the current OpenSPG 0.8 workflow and toolchain.​

🔧 1. Start the OpenSPG Core Engine
If you already ran Docker successfully:

bash
docker-compose -f docker-compose.yml up -d
Ensure all four containers are up:

openspg-server → manages schema, rules, and APIs

openspg-mysql → stores schema and metadata

tugraph → graph data backend

elasticsearch → index for retrieval

Then confirm that the web frontend is live at:

text
http://127.0.0.1:8887
You should see the visual schema editor and service dashboard.​

🧰 2. Set Up the KAG (Knowledge Augmented Generation) Toolkit
OpenSPG’s reasoning and querying layer is provided via KAG (a companion package for semantic reasoning and LLM integration).

Install KAG inside a Python 3.10+ virtual environment:

bash
git clone https://github.com/OpenSPG/KAG.git
cd KAG
pip install -e .
Verify installation:

bash
knext --version
You should see something like knext 0.8.0.​

🧩 3. Configure a Knowledge Project
Now, define your local Knowledge Base (KB) that binds together vectorizers, models, and data.

Inside the folder KAG/examples, copy and edit a config file:

bash
cp examples/example_config.yaml my_config.yaml
vim my_config.yaml
Example configuration:

text
openie_llm:
  api_key: sk-<your-openai-key>
  base_url: https://api.openai.com/v1
  model: gpt-5-mini
  type: maas

vectorizer:
  api_key: sk-<your-openai-key>
  base_url: https://api.openai.com/v1
  model: text-embedding-3-small
  type: openai
  vector_dimensions: 1536

project:
  id: "1"
  host_addr: http://127.0.0.1:8887
  language: en
  namespace: my_local_kb
Then initialize the project:

bash
cd examples
knext project create --prj_path .
knext schema commit
📥 4. Import and Vectorize Data
Upload or import knowledge sources (CSV, TXT, JSONL):

bash
knext builder execute \
  --pipeline ./pipelines/builder.yaml \
  --inputs ./data/*.txt
This automatically generates and stores entity & relation embeddings using the configured vectorizer.​

You can inspect ingestion logs in:

text
logs/builder.log
⚙️ 5. Run Inference and Reasoning
After data ingestion, you can run reasoning logic or Q&A queries:

bash
knext reasoner execute \
  --config ./configs/reason.yaml \
  --query "How is entity A related to concept B?"
You can also access the reasoning web client through:

text
http://127.0.0.1:8887/reasoner
🧾 6. Optional: Integrate LLM Reasoning (KG + LLM Fusion)
In the config file, add a section linking an LLM model for fusion logic:

text
reason_llm:
  api_key: sk-<your-openai-key>
  base_url: https://api.openai.com/v1
  model: gpt-5
  type: maas
Then run:

bash
knext thinker execute --query "Summarize insights about topic X using the KB."
This uses neural‑symbolic fusion reasoning, combining graph logic with LLM generation.​

✅ 7. Verify the Setup
After completing the above:

Open http://127.0.0.1:8887 — UI ready.

Run knext --help — CLI recognized.

Confirm vector embeddings exist under /data/vector_store.

Test a reasoning query — if it returns text, OpenSPG and KAG are functioning.

🧭 In Summary
Step	Action	Outcome
1	Start Docker containers	OpenSPG core server active
2	Install KAG toolkit	Command‑line interface available
3	Create KB config	Vectorizer + model linked
4	Import data	Documents stored + embedded
5	Run reasoner	Logical/semantic answers
6	(Optional) LLM fusion	KB + LLM reasoning
7	Verify UI & logs	Full setup ready
Following these steps will bring your local OpenSPG (KAG 0.8) environment fully online for document ingestion, knowledge graph construction, and reasoning in 2025.​