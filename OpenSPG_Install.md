# 1 Pre-Requirements 

## 1.1 Hardware Requirements
CPU ≥ 8 cores;
RAM ≥ 32 GB;
Disk ≥ 100 GB;

## 1.2 Software Requirements  

### Operating System 
macOS System：macOS Monterey 12.6 or later
Linux System：CentOS 7 / Ubuntu 20.04 or later
Windows System：Windows 10 LTSC 2021 or later

### Application software 
macOS / Linux System：Docker，Docker Compose
Windows System：WSL 2 / Hyper-V，Docker，Docker Compose

Docker ≥ 24.0.0 & Docker Compose ≥ v2.26.1.

## 1.3 Generate model

KAG supports all generative model services with OpenAI-compatible class interfaces, such as DeepSeek, Qwen, OpenAI, etc.
Developers can go to the official websites of large commercial models such as deepseek official website, tongyi official website, openai official website to complete account registration and activation of model services in advance, obtain the api-key, and fill it in the subsequent project configuration.

KAG also supports docking with the generative model prediction services provided by Ollama, Xinference, etc. For details, please refer to the relevant chapters on model services. In the quick start stage, it is strongly recommended to purchase a commercial large model API to complete the trial run verification.

## 1.4 Representation model 
KAG supports representation model services with OpenAI-compatible class interfaces, such as OpenAI, Silicon Mobility, etc.
Developers can go to the official website of Silicon flow website, openai official website and other commercial model websites to complete account registration and activation of model services in advance, obtain the API key, and fill it in the subsequent project configuration.

KAG also supports docking with representation model prediction services provided by Ollama, Xinference, etc. For details, please refer to the relevant chapters on model services. In the quick start stage, it is strongly recommended to purchase a commercial large model API to complete the trial run verification.

# 2 Service deployment
## 2.1 Start the service

# set HOME enviroment var（only for Windows Users）
# set HOME=%USERPROFILE%
# get docker-compose.yaml file
$ curl -sSL https://raw.githubusercontent.com/OpenSPG/openspg/refs/heads/master/dev/release/docker-compose-west.yml -o docker-compose-west.yml
# service start
$ docker compose -f docker-compose-west.yml up -d

Tip: If you want to persist data in a local directory, you can do this through Docker's volumes configuration. This way, the data will not be lost even if the container is restarted or deleted. Add the following content to the volumes of mysql and neo4j in docker-compose.yml


## 2.2 View Status
$ docker ps

$ docker logs -f release-openspg-server
The following log shows the successful start of the openspg server

## 2.3 Product Access

Enter http://127.0.0.1:8887 in the browser to access the OpenSPG-KAG product interface.
# Default login information:
# Default Username: openspg
# Default password: openspg@kag

# The default password must be changed before it can be used. 
# If you forget the password, you can reinitialize it in the database with the following command:


UPDATE kg_user SET `gmt_create` = now(),`gmt_modified` = now(),`dw_access_key` ='efea9c06f9a581fe392bab2ee9a0508b2878f958c1f422f8080999e7dc024b83' where user_no = 'openspg' limit 1;

# 3 KAG usage (product mode) 

This product provides a visual interface for OpenSPG-KAG, supporting users to build, ask and manage private domain knowledge bases on the page. At the same time, the modeling results can be viewed intuitively.
When used in production mode, the KAG package python package is built into the openspg container, providing default building and reasoning question-answering capabilities. The calls to the generation model and representation model in the knowledge extraction and graph reasoning stages are all initiated from the openspg server container environment.
https://openspg.yuque.com/ndx6g9/0.5/nbb1bn3wegwue6yo?inner=zb7FU

## 3.1 Model Configuration

KAG Supports Open-AI compatible generative Model APIs (chatgpt, deepseek, qwen2, etc.)，provides maas, vllm, ollama and other modes, for details, refer to.  It is generally recommended that the knowledge question answering model use a 72B scale, and the knowledge extraction model use a 7B scale.

● Example of configuring a business presentation model service such as Silicon Mobility:
{
  "type": "openai",
  "model": "BAAI/bge-m3",
  "base_url": "https://api.siliconflow.cn/v1",
  "api_key": "YOUR_API_KEY",
  "vector_dimensions": "1024"
}
● Model service availability testing
When the configuration is saved, kag will call the large model API according to the representation model configuration. If the call fails, it will prompt that the save failed. Users can use the curl command in the openspg container to verify the service accessibility and whether the api-key has expired.

$ curl --request POST \
  --url https://api.siliconflow.cn/v1/embeddings \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "BAAI/bge-large-zh-v1.5",
    "input": "Silicon-based mobile embedding is now available. Come and try it out!",
    "encoding_format": "float"
  }'
3.2 New Knowledge Base 

### 3.2.1 Basic Configuration

● Chinese name of knowledge base
Required. The Chinese name of the knowledge base, used for page display
● English name of knowledge base
Required. The English name of the knowledge base must start with a capital letter and can only be a combination of letters and numbers, with a minimum of 3 characters. Used for schema prefixes and graph storage data isolation
● Whether public
Required. Set knowledge base visibility (default: Private, visible only to creator).
● Knowledge Base Type
Required. Default: Local
  ○ Local: Requires uploading files to build the knowledge base
  ○ External Network Knowledge Base: Accesses external knowledge via MCP protocol
● Figure Storage Configuration
Parameter name	Parameter Description database	

- The database name of the graph storage is fixed and consistent with the English name of the knowledge base and cannot be modified
password	

- The default value of the built-in openspg-neo4j is: neo4j@openspg
uri	

- The default value of the built-in openspg-neo4j is: neo4j://release-openspg-neo4j:7687
user	

- mThe default value of the built-in openspg-neo4j is: neo4j

● Vector configuration
Provides vector generation service, supports bge and openai-embedding. It is recommended to use bge-m3 for English and bge-base-zh for Chinese. For details, refer to Embedding Model Configuration.
If the vector model is changed, a new knowledge base must be created.

● Prompt words in Chinese and English
Used to determine whether to use Chinese (zh) or English (en) when calling the model. Example:

## 3.3 Import documents 

### 3.3.1 Create a build task
Enter the knowledge base Build => Create task to initiate knowledge building tasks. Users can download sample files     for multi-hop Q&A tasks testing.

The extraction model used for knowledge construction and the reasoning model used for knowledge question answering can be models of different specifications. We tested a hybrid solution of 7B model for knowledge construction and 72B model for knowledge question answering. The results on the three lists of two_wiki, hotpotqa and musique only slightly decreased by 1.20%, 1.90% and 3.11%, but the token cost of building a 100,000-word document (Alibaba Cloud Bailian) was reduced from 4.63￥ to 0.479￥, a reduction of 89%, which can greatly save users' time and financial costs.

### 3.3.2 Check knowledge extraction Results
Users can view the graph data by clicking on the [Knowledge Exploration] menu on the product side.
Users can refer to Knowledge Exploration doc for detail.



3.4 Reasoning Questions and Answers 
Enter the question Which Stanford University professor works on Alzheimer's? and wait for the result to return. 

4 KAG usage (developer mode)
In the context of private domain knowledge bases, the effectiveness of graph construction and reasoning-based question answering is closely tied to schema design, knowledge extraction prompts, the selection of representation models, question planning prompts, graph retrieval algorithms, and answer generation prompts. These customizations are not yet exposed on the product side, requiring users to leverage the KAG developer mode to implement their customizations.

When using the developer mode, users execute the KAG Python package code in their local environment. The OpenSPG server solely provides capabilities such as schema management, reasoning execution, and graph database adaptation. Calls to generative models and representation models during the knowledge extraction and graph reasoning phases are initiated from the local environment.
https://openspg.yuque.com/ndx6g9/0.5/nbb1bn3wegwue6yo?inner=S8PoP


4.0、Video Tutorial

4.1 Environment configuration 

4.1.1 Pre-dependency
● OpenSPG-Server 
KAG relies on OpenSPG-Server for metadata management and image storage services. Refer to the first and second parts of this document to complete the server deployment.

4.1.2 Virtual Environment Installation
# Install conda
# conda installation ：https://docs.anaconda.com/miniconda/


# Install python virtual env：
$ conda create -n kag-demo python=3.10 && conda activate kag-demo
4.2 Code Clone

# code clone：
$ git clone https://github.com/OpenSPG/KAG.git

# KAG installation: 
$ cd ./KAG && pip install -e .

# confirmation
$ knext --version
$ knext --help
Usage: knext [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  project   Project client.
  reasoner  Reasoner client.
  schema    Schema client.
  thinker   Thinker client.
4.3 Create a knowledge base
4.3.1 New Project 
● enter the project examples Directory
$ cd kag/examples
● edit Project Configuration
$ vim ./example_config.yaml
#------------project configuration start----------------#
openie_llm: &openie_llm
  api_key: key
  base_url: https://api.deepseek.com
  model: deepseek-chat
  type: maas

chat_llm: &chat_llm
  api_key: key
  base_url: https://api.deepseek.com
  model: deepseek-chat
  type: maas

vectorize_model: &vectorize_model
  api_key: key
  base_url: https://api.siliconflow.cn/v1/
  model: BAAI/bge-m3
  type: openai
  vector_dimensions: 1024
vectorizer: *vectorize_model

log:
  level: INFO

project:
  biz_scene: default
  host_addr: http://127.0.0.1:8887
  id: "1"
  language: en
  namespace: TwoWikiTest
#------------project configuration end----------------#

#------------kag-builder configuration start----------------#
kag_builder_pipeline:
  chain:
    type: unstructured_builder_chain # kag.builder.default_chain.DefaultUnstructuredBuilderChain
    extractor:
      type: schema_free_extractor # kag.builder.component.extractor.schema_free_extractor.SchemaFreeExtractor
      llm: *openie_llm
      ner_prompt:
        type: default_ner # kag.builder.prompt.default.ner.OpenIENERPrompt
      std_prompt:
        type: default_std # kag.builder.prompt.default.std.OpenIEEntitystandardizationdPrompt
      triple_prompt:
        type: default_triple # kag.builder.prompt.default.triple.OpenIETriplePrompt
    reader:
      type: dict_reader # kag.builder.component.reader.dict_reader.DictReader
    post_processor:
      type: kag_post_processor # kag.builder.component.postprocessor.kag_postprocessor.KAGPostProcessor
    splitter:
      type: length_splitter # kag.builder.component.splitter.length_splitter.LengthSplitter
      split_length: 100000
      window_length: 0
    vectorizer:
      type: batch_vectorizer # kag.builder.component.vectorizer.batch_vectorizer.BatchVectorizer
      vectorize_model: *vectorize_model
    writer:
      type: kg_writer # kag.builder.component.writer.kg_writer.KGWriter
  num_threads_per_chain: 1
  num_chains: 16
  scanner:
    type: 2wiki_dataset_scanner # kag.builder.component.scanner.dataset_scanner.MusiqueCorpusScanner
#------------kag-builder configuration end----------------#

#------------kag-solver configuration start----------------#
search_api: &search_api
  type: openspg_search_api #kag.solver.tools.search_api.impl.openspg_search_api.OpenSPGSearchAPI

graph_api: &graph_api
  type: openspg_graph_api #kag.solver.tools.graph_api.impl.openspg_graph_api.OpenSPGGraphApi

kg_cs:
  type: kg_cs_open_spg
  path_select:
    type: exact_one_hop_select
    graph_api: *graph_api
    search_api: *search_api
  entity_linking:
    type: entity_linking
    graph_api: *graph_api
    search_api: *search_api
    recognition_threshold: 0.9
    exclude_types:
      - "Chunk"

kg_fr:
  type: kg_fr_open_spg
  top_k: 20
  path_select:
    type: fuzzy_one_hop_select
    llm_client: *chat_llm
    graph_api: *graph_api
    search_api: *search_api
  ppr_chunk_retriever_tool:
    type: ppr_chunk_retriever
    llm_client: *ner_llm
    graph_api: *graph_api
    search_api: *search_api
  entity_linking:
    type: entity_linking
    graph_api: *graph_api
    search_api: *search_api
    recognition_threshold: 0.8
    exclude_types:
      - "Chunk"

rc:
  type: rc_open_spg
  vector_chunk_retriever:
    type: vector_chunk_retriever
    vectorize_model: *vectorize_model
    search_api: *search_api
  graph_api: *graph_api
  search_api: *search_api
  vectorize_model: *vectorize_model
  top_k: 20

kag_merger:
  type: kg_merger
  top_k: 20
  llm_module: *chat_llm
  summary_prompt:
    type: default_thought_then_answer
  vectorize_model: *vectorize_model
  graph_api: *graph_api
  search_api: *search_api

kag_hybrid_executor: &kag_hybrid_executor_conf
  type: kag_hybrid_executor
  lf_rewriter:
    type: kag_spo_lf
    llm_client: *openie_llm
    lf_trans_prompt:
      type: default_spo_retriever_decompose
    vectorize_model: *vectorize_model
  flow: |
    kg_cs->kg_fr->kag_merger;rc->kag_merger

kag_output_executor: &kag_output_executor_conf
  type: kag_output_executor
kag_deduce_executor: &kag_deduce_executor_conf
  type: kag_deduce_executor

py_code_based_math_executor: &py_code_based_math_executor_conf
  type: py_code_based_math_executor
  llm: *openie_llm

kag_solver_pipeline:
  type: kag_static_pipeline
  planner:
    type: lf_kag_static_planner
    llm: *chat_llm
    plan_prompt:
      type: default_lf_static_planning
    rewrite_prompt:
      type: default_rewrite_sub_task_query
  executors:
    - *kag_hybrid_executor_conf
    - *py_code_based_math_executor_conf
    - *kag_deduce_executor_conf
    - *kag_output_executor_conf
  generator:
    type: llm_generator
    llm_client: *chat_llm
    generated_prompt:
      type: default_multi_hop_generator
#------------kag-solver configuration end----------------#
Please remember to fill in the api_key field of chat_llmand openie_llm with your DeepSeek API key, and fill in the api_key field of vectorize_model with your SiliconFlow API key.
The extraction model for knowledge construction, openie_llm, and the reasoning model for knowledge question answering, chat_llm, can be models of different specifications. We tested a hybrid approach using a 7B model for knowledge construction and a 72B model for knowledge question answering. The performance on the two_wiki, hotpotqa, and musique benchmarks only saw minor declines of 1.20%, 1.90%, and 3.11%, respectively. However, the token cost for constructing a 100,000-character document (on Aliyun's Bailian platform) decreased from 4.63￥ to 0.479￥, a reduction of 89%, significantly saving users both time and financial costs.
● create Project (One-to-one mapping with the knowledge base in the product): 
$ knext project create --config_path ./example_config.yaml
● directory Initialization 
After creating a project, a directory with the same name as the namespace field in the project configuration (e.g., TwoWikiTest in the example) will be created under the kag/examples directory, and the KAG project code framework will be initialized.

Users can modify one or more of the following files to customize the business-specific knowledge graph construction and reasoning-based question answering.
TwoWikiTest
  ├── builder
  │   ├── data
  │   ├── indexer.py
  │   └── prompt
  │   		├── ner.py
  │   		├── std.py
  │   		└── tri.py
  ├── kag_config.cfg
  ├── reasoner
  ├── schema
  │   ├── TwoWikiTest.schema
  └── solver
      ├── evaForHotpotqa.py
      └── prompt
          ├── logic_form_plan.py
          └── resp_generator.py
4.3.2 update the project (Optional)
If there are any configuration changes, you may refer to the content of this section to update the configuration  on the server side.
● enter the project examples Directory 
$ cd kag/examples/TwoWikiTest
● edit Project Configuration
Note: Due to the varying usage of different representation models, it is not recommended to update the vectorizer configuration after the project has been created. If there is a need to update the vectorizer configuration, it is advised to create a new project instead.
$ vim ./kag_config.yaml
Once again, please ensure that all api-key fields have been correctly filled in.
● run command: 
$ knext project update --proj_path ./
4.4 Import documents 
● Enter the project directory
$ cd kag/examples/TwoWikiTest
● Obtain the corpus file
The test corpus data for the 2wiki dataset is located at open_benchmark/2wiki/builder/data/corpus.json, which contains 6,119 documents and 1,000 question-answer pairs. To quickly run through the entire process, there is also a sub_corpus.json file in the directory, which includes only 3 documents. We will use this smaller dataset as an example for experimentation.  
Copy the corpus file to the corresponding directory in the TwoWikiTest project:
$ cp ../../open_benchmark/2wiki/builder/data/sub_corpus.json builder/data/
● Edit schema(Optional)  
User can refere to  to customize schema/TwoWikiTest.schema file.
● Submit the updated schema to SPG server
$ knext schema commit
● Execute the build task.
Define the build script in the builder/indexer.py file:
$ vim ./builder/indexer.py
import argparse
import os
import logging
import asyncio
from kag.common.registry import import_modules_from_path

from kag.builder.runner import BuilderChainRunner

logger = logging.getLogger(__name__)


async def buildKB(file_path):
    from kag.common.conf import KAG_CONFIG

    runner = BuilderChainRunner.from_config(
        KAG_CONFIG.all_config["kag_builder_pipeline"]
    )
    await runner.ainvoke(file_path)

    logger.info(f"\n\nbuildKB successfully for {file_path}\n\n")


if __name__ == "__main__":
    import_modules_from_path(".")
    parser = argparse.ArgumentParser(description="args")
    parser.add_argument(
        "--corpus_file",
        type=str,
        help="test file name in /data",
        default="data/sub_corpus.json",
    )

    args = parser.parse_args()
    file_path = args.corpus_file

    dir_path = os.path.dirname(__file__)
    file_path = os.path.join(dir_path, file_path)

    asyncio.run(buildKB(file_path))

● Builder Chain running 
Run theindexer.py script to complete the graph construction of unstructured data
$ cd builder
$ python ./indexer.py
Once the build script is launched, a checkpoint directory for the task will be generated under the current working directory(i.e., ./builder), recording the checkpoints and statistical information of the construction pipeline.
builder
├── ckpt
│   ├── chain
│   ├── extractor
│   ├── kag_checkpoint_0_1.ckpt
│   ├── postprocessor
│   ├── reader
│   └── splitter
├── data
│   ├── sub_corpus.json
├── indexer.py
Use the following command to view the statistical information of the extraction task, such as how many nodes/edges are extracted from each document:
$ less ckpt/kag_checkpoint_0_1.ckpt

Use the following command to check how many document entries have been successfully processed and written to the graph database:
$ wc -l ckpt/kag_checkpoint_0_1.ckpt

The KAG framework provides a checkpoint-based resumption feature. If the task is interrupted due to program errors or other external reasons (such as insufficient LLM balance), you can re-execute indexer.py. KAG will automatically detect the checkpoint files and reuse the existing results.
● Result Inspection
Currently, KAG offers knowledge exploration capabilities on the product side, along with the corresponding API documentation.



4.5 Reasoning Questions and Answers
● Enter the project directory
cd kag/examples/TwoWikiTest
● Edit the QA script
$ cp ../../open_benchmark/2wiki/solver/data/qa_sub.json solver/data/
$ vim ./solver/qa.py
Paste the following content into eva.py.
import json
import logging
import os
from typing import List

from kag.common.benchmarks.evaluate import Evaluate
from kag.examples.utils import delay_run
from kag.open_benchmark.utils.eval_qa import EvalQa, running_paras, do_main
from kag.common.conf import KAG_CONFIG
from kag.common.registry import import_modules_from_path
from kag.interface import SolverPipelineABC
from kag.solver.reporter.trace_log_reporter import TraceLogReporter

logger = logging.getLogger(__name__)


class EvaFor2wiki(EvalQa):
    """
    init for kag client
    """

    def __init__(self, solver_pipeline_name="kag_solver_pipeline"):
        super().__init__(task_name="2wiki", solver_pipeline_name=solver_pipeline_name)

    async def qa(self, query, gold):
        reporter: TraceLogReporter = TraceLogReporter()

        pipeline = SolverPipelineABC.from_config(
            KAG_CONFIG.all_config[self.solver_pipeline_name]
        )
        answer = await pipeline.ainvoke(query, reporter=reporter, gold=gold)

        logger.info(f"\n\nso the answer for '{query}' is: {answer}\n\n")

        info, status = reporter.generate_report_data()
        return answer, {"info": info.to_dict(), "status": status}

    async def async_process_sample(self, data):
        sample_idx, sample, ckpt = data
        question = sample["question"]
        gold = sample["answer"]
        try:
            if ckpt and question in ckpt:
                print(f"found existing answer to question: {question}")
                prediction, trace_log = ckpt.read_from_ckpt(question)
            else:
                prediction, trace_log = await self.qa(query=question, gold=gold)
                if ckpt:
                    ckpt.write_to_ckpt(question, (prediction, trace_log))
            metrics = self.do_metrics_eval([question], [prediction], [gold])
            return sample_idx, prediction, metrics, trace_log
        except Exception as e:
            import traceback

            logger.warning(
                f"process sample failed with error:{traceback.print_exc()}\nfor: {sample['question']} {e}"
            )
            return None

    def load_data(self, file_path):
        with open(file_path, "r") as f:
            return json.load(f)

    def do_metrics_eval(self, questionList: List[str], predictions: List[str], golds: List[str]):
        eva_obj = Evaluate()
        return eva_obj.getBenchMark(questionList, predictions, golds)

    def do_recall_eval(self, sample, references):
        eva_obj = Evaluate()
        paragraph_support_idx_set = [
            idx["paragraph_support_idx"] for idx in sample["question_decomposition"]
        ]
        golds = []
        for idx in paragraph_support_idx_set:
            golds.append(
                eva_obj.generate_id(
                    sample["paragraphs"][idx]["title"],
                    sample["paragraphs"][idx]["paragraph_text"],
                )
            )
        return eva_obj.recall_top(predictionlist=references, goldlist=golds)


if __name__ == "__main__":
    import_modules_from_path("./prompt")
    delay_run(hours=0)
    # 解析命令行参数
    parser = running_paras()
    args = parser.parse_args()
    qa_file_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), f"{args.qa_file}"
    )
    do_main(
        qa_file_path=qa_file_path,
        thread_num=args.thread_num,
        upper_limit=args.upper_limit,
        collect_file=args.res_file,
        eval_obj=EvaFor2wiki(),
    )
● Execute the QA script:
$ cd solver
$ python eva.py --qa_file ./data/qa_sub.json
4.6 Other built-in cases
you can enter the kag/examples directory to experience the cases brought in the source code. 







4.7、FAQ
Please refer to the FAQ section for details on how to view checkpoint content and customize extraction & QA task-related information.