---
title: "Chain of Draft: Thinking Faster by Writing Less"
source: "https://arxiv.org/html/2502.18600v2"
author:
published:
created: 2025-03-08
description:
tags:
  - "clippings"
---
Silei Xu, Wenhao Xie, Lingxiao Zhao, Pengcheng He  
Zoom Communications  

###### Abstract

Large Language Models (LLMs) have demonstrated remarkable performance in solving complex reasoning tasks through mechanisms like Chain-of-Thought (CoT) prompting, which emphasizes verbose, step-by-step reasoning. However, humans typically employ a more efficient strategy: drafting concise intermediate thoughts that capture only essential information. In this work, we propose Chain of Draft (CoD), a novel paradigm inspired by human cognitive processes, where LLMs generate minimalistic yet informative intermediate reasoning outputs while solving tasks. By reducing verbosity and focusing on critical insights, CoD matches or surpasses CoT in accuracy while using as little as only 7.6% of the tokens, significantly reducing cost and latency across various reasoning tasks. Our code and data are available at [https://github.com/sileix/chain-of-draft](https://github.com/sileix/chain-of-draft).

Chain of Draft: Thinking Faster by Writing Less

Silei Xu<sup class="ltx_note_mark">†</sup><sup class="ltx_note_mark">†</sup>thanks: Correspondence to <silei.xu@zoom.us\>, Wenhao Xie, Lingxiao Zhao, Pengcheng He Zoom Communications

## 1 Introduction

Recent advances in reasoning models such as OpenAI o1 [^17] and DeepSeek R1 [^9] have propelled large language models (LLMs) to unprecedented performance on complex tasks using techniques like Chain of Thought (CoT) [^22]. This paradigm encourages models to break down problems into step-by-step explorations, mimicking the structured reasoning process of humans. While effective, this approach demands substantially more computational resources at inference time, leading to verbose outputs and higher latency. Such verbosity contrasts sharply with how humans typically approach problem-solving: we rely on concise drafts or shorthand notes to capture essential insights without unnecessary elaboration.

Motivated by this difference, we propose Chain of Draft (CoD), a novel prompting strategy that aligns more closely with human reasoning by prioritizing efficiency and minimalism. Instead of verbose intermediate steps, Chain of Draft encourages LLMs to generate concise, dense-information outputs at each step. This approach reduces latency and computational costs without sacrifice of accuracy, making LLMs more practical for real-world applications where efficiency is paramount.

![Refer to caption](https://arxiv.org/html/2502.18600v2/extracted/6244873/plot.png)

Figure 1: Figure 1: Comparison of Claude 3.5 Sonnet’s accuracy and token usage across different tasks with three different prompt strategies: direct answer (Standard), Chain of Thought (CoT), and Chain of Draft (CoD). CoD achieves similar accuracy as CoT while using significant fewer tokens.

The intuition behind Chain of Draft is rooted in how humans externalize thought. When solving complex tasks — whether solving mathematical problems, drafting essays, or coding — we often jot down only the critical pieces of information that help us progress. By emulating this behavior, LLMs can focus on advancing toward solutions without the overhead of verbose reasoning.

To evaluate the effectiveness of Chain of Draft, we conducted experiments across a variety of benchmarks requiring multi-step reasoning, including arithmetic reasoning, common sense reasoning, and symbolic reasoning. Our results demonstrate that this minimalist approach maintains or even improves accuracy compared with standard Chain of Thought, while significantly reducing token usage and latency.

The contributions of this paper are threefold:

- •

We introduce Chain of Draft, a concise reasoning prompting strategy inspired by human cognitive processes.
- •

We empirically validate that Chain of Draft can achieve significantly reduced latency and cost without sacrificing accuracy.
- •

We discuss the implications of Chain of Draft for LLM design, deployment, and real-world usability.

## 2 Related Work

Structured Reasoning Frameworks for LLMs Recently, a variety of reasoning language models have emerged, including o1 by OpenAI [^17], QwQ by Alibaba [^19], and R1 by DeepSeek [^9], demonstrating substantial improvements in tackling complex tasks. These models leverage structured reasoning methods to enhance robustness and problem-solving capabilities. The concept of Chain-of-Thought reasoning (CoT) [^22], established a foundational approach to reasoning in LLMs. Building on this foundation, more sophisticated topologies have emerged, such as tree [^24] and graph [^2], enabling LLMs to address increasingly intricate problems.

Other enhancements include self-consistency CoT [^21], which incorporates verification and reflection mechanisms to bolster reasoning reliability, and ReAct [^25], which integrates tool usage into the reasoning process, allowing LLMs to access external resources and knowledge. These innovations collectively expand the reasoning capabilities of LLMs across a diverse range of applications.

LLM Inference Latency Reduction Although structured reasoning greatly enhances LLMs’ ability to solve complex questions, it significantly increases the token usage before arriving at a final answer. This makes it challenging to apply in cost-sensitive and latency-sensitive scenarios [^20]. Furthermore, the model’s lack of awareness regarding task complexity often leads to overthinking [^5] even on simple tasks, resulting in unnecessary resource consumption.

Techniques like streaming aim to reduce perceived latency by incrementally providing partial outputs as they are generated, rather than waiting for the entire output sequence. However, this approach cannot fully mitigate overall latency or computational cost, and it is often unsuitable for chain-of-thought reasoning, as intermediate steps are often not intended to be shown to end users.

[^16] proposes Skeleton-of-Thought (SoT), a method that first guides LLMs to generate a skeleton outline of the answer, followed by parallel decoding to reduce latency. While SoT helps lower latency, it does not reduce computational cost and is limited to questions that can be parallelized effectively. [^27] took a different approach, it first generates draft tokens at lower quality but higher speed through selective skipping of intermediate layers, and then validates the draft in a single forward pass. Our approach, CoD, can be combined with these approaches to further reduce the latency.

[^11] proposes Coconut to train LLMs to perform reasoning in a continuous latent space rather than in the traditional natural language space using the final hidden state of the LLM to represent the reasoning process. While Coconut reduces latency and computational cost, it suffers from reduced accuracy in complex tasks, such as GSM8k. Additionally, it loses the interpretability of natural language reasoning and cannot be applied to black-box models like GPT and Claude.

The works closest to ours are Concise Thoughts (CCoT) [^15] and token-budget-aware LLM reasoning (TALE) [^10]. CCoT proposes using a fixed global token budget for reasoning steps. However, different tasks may require varying budgets to achieve the optimal balance between performance and cost. Moreover, LLMs may fail to adhere to an impractical budget, often generating far more tokens than intended [^10]. [^10] extends this idea by dynamically estimating a global token budget for different problems based on reasoning complexity. However, this approach requires an additional LLM call to estimate the budget, which increases latency. Furthermore, it assumes that the model can accurately predict the complexity of requests, limiting its applicability to more complex tasks where reflection, self-correction, or external knowledge retrieval may be necessary during the reasoning process. In contrast, our approach employs a per-step budget, allowing unlimited reasoning steps, which makes it more adaptable to various structured reasoning techniques.

## 3 Chain-of-Draft Prompting

The Chain-of-Thought (CoT) prompting strategy has demonstrated significant effectiveness across a wide range of tasks, particularly those requiring complex multi-step reasoning. However, LLMs often produce excessively verbose reasoning steps, consuming a substantial number of tokens before arriving at a final answer. In contrast, humans tend to adopt a more concise approach when solving complex problems involving multi-step reasoning, such as mathematical or logical puzzles. Rather than elaborating on every detail, humans typically jot down only the essential intermediate results — minimal drafts — to facilitate their thought processes. Inspired by this natural tendency, we propose a novel prompting strategy called Chain-of-Draft (CoD). This approach aims to reduce verbosity by limiting the number of words used in each reasoning step, focusing only on the essential calculations or transformations needed to progress.

To illustrate the difference between standard prompting, Chain-of-Thought prompting, and our proposed Chain-of-Draft prompting, consider the following simple arithmetic problem:

Q: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?

The response generated by a standard prompting approach directly outputs the answer, often without any reasoning. While correct, this lacks transparency in how the answer was derived, and requires the language model to run multi-step reasoning without any help from intermediate result, which often leads to hallucination.

<svg class="ltx_picture" height="107.14" id="S3.1.p1.pic1" overflow="visible" version="1.1" width="270"><g fill="#000000" stroke="#000000" stroke-width="0.4pt" transform="translate(0,107.14) matrix(1 0 0 -1 0 0)"><g fill="#BFBFBF" fill-opacity="1.0"><path d="M 0 5.91 L 0 101.23 C 0 104.49 2.64 107.14 5.91 107.14 L 264.09 107.14 C 267.35 107.14 270 104.49 270 101.23 L 270 5.91 C 270 2.64 267.35 0 264.09 0 L 5.91 0 C 2.64 0 0 2.64 0 5.91 Z"></path></g><g fill="#F2F2F2" fill-opacity="1.0"><path d="M 1.97 5.91 L 1.97 93.59 L 268.03 93.59 L 268.03 5.91 C 268.03 3.73 266.27 1.97 264.09 1.97 L 5.91 1.97 C 3.73 1.97 1.97 3.73 1.97 5.91 Z"></path></g><g fill-opacity="1.0" transform="matrix(1.0 0.0 0.0 1.0 17.72 95.56)"><foreignObject color="#FFFFFF" height="9.61" overflow="visible" transform="matrix(1 0 0 -1 0 16.6)" width="234.57"><span class="ltx_inline-block ltx_minipage ltx_align_bottom" id="S3.1.p1.pic1.1.1.1.1.1"><span class="ltx_p" id="S3.1.p1.pic1.1.1.1.1.1.1"><span class="ltx_text ltx_font_typewriter" id="S3.1.p1.pic1.1.1.1.1.1.1.1">Standard</span></span> </span></foreignObject></g><g fill-opacity="1.0" transform="matrix(1.0 0.0 0.0 1.0 17.72 9.84)"><foreignObject color="#000000" height="75.87" overflow="visible" transform="matrix(1 0 0 -1 0 16.6)" width="234.57"><span class="ltx_inline-block ltx_minipage ltx_align_bottom" id="S3.1.p1.pic1.2.2.2.1.1"><span class="ltx_p" id="S3.1.p1.pic1.2.2.2.1.1.1"><span class="ltx_text ltx_font_typewriter" id="S3.1.p1.pic1.2.2.2.1.1.1.1">Q: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?<br class="ltx_break">A: 8</span></span></span></foreignObject></g></g></svg>

Chain-of-Thought prompting, on the other hand, provides a detailed reasoning process. While this response is accurate and interpretable, it includes unnecessary details about Jason, Denny, and the lollipops, which are irrelevant to solving the mathematical problem. This verbosity inflates the token count and increases the response latency.

<svg class="ltx_picture" height="411.55" id="S3.2.p1.pic1" overflow="visible" version="1.1" width="270"><g fill="#000000" stroke="#000000" stroke-width="0.4pt" transform="translate(0,411.55) matrix(1 0 0 -1 0 0)"><g fill="#BFBFBF" fill-opacity="1.0"><path d="M 0 5.91 L 0 405.64 C 0 408.91 2.64 411.55 5.91 411.55 L 264.09 411.55 C 267.35 411.55 270 408.91 270 405.64 L 270 5.91 C 270 2.64 267.35 0 264.09 0 L 5.91 0 C 2.64 0 0 2.64 0 5.91 Z"></path></g><g fill="#F2F2F2" fill-opacity="1.0"><path d="M 1.97 5.91 L 1.97 395.31 L 268.03 395.31 L 268.03 5.91 C 268.03 3.73 266.27 1.97 264.09 1.97 L 5.91 1.97 C 3.73 1.97 1.97 3.73 1.97 5.91 Z"></path></g><g fill-opacity="1.0" transform="matrix(1.0 0.0 0.0 1.0 17.72 397.28)"><foreignObject color="#FFFFFF" height="12.3" overflow="visible" transform="matrix(1 0 0 -1 0 16.6)" width="234.57"><span class="ltx_inline-block ltx_minipage ltx_align_bottom" id="S3.2.p1.pic1.1.1.1.1.1"><span class="ltx_p" id="S3.2.p1.pic1.1.1.1.1.1.1"><span class="ltx_text ltx_font_typewriter" id="S3.2.p1.pic1.1.1.1.1.1.1.1">Chain-of-Thought</span></span> </span></foreignObject></g><g fill-opacity="1.0" transform="matrix(1.0 0.0 0.0 1.0 17.72 9.84)"><foreignObject color="#000000" height="377.6" overflow="visible" transform="matrix(1 0 0 -1 0 16.6)" width="234.57"><span class="ltx_inline-block ltx_minipage ltx_align_bottom" id="S3.2.p1.pic1.2.2.2.1.1"><span class="ltx_p" id="S3.2.p1.pic1.2.2.2.1.1.1"><span class="ltx_text ltx_font_typewriter" id="S3.2.p1.pic1.2.2.2.1.1.1.1">Q: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?<br class="ltx_break">A: Let’s think through this step by step:</span></span> <span class="ltx_p" id="S3.2.p1.pic1.2.2.2.1.1.2"><span class="ltx_text ltx_font_typewriter" id="S3.2.p1.pic1.2.2.2.1.1.2.1">1. Initially, Jason had 20 lollipops.<br class="ltx_break">2. After giving some to Denny, Jason now has 12 lollipops.<br class="ltx_break">3. To find out how many lollipops Jason gave to Denny, we need to calculate the difference between the initial number of lollipops and the remaining number.<br class="ltx_break">4. We can set up a simple subtraction problem: Initial number of lollipops - Remaining number of lollipops = Lollipops given to Denny<br class="ltx_break">5. Putting in the numbers: 20 - 12 = Lollipops given to Denny<br class="ltx_break">6. Solving the subtraction: 20 - 12 = 8</span></span> <span class="ltx_p" id="S3.2.p1.pic1.2.2.2.1.1.3"><span class="ltx_text ltx_font_typewriter" id="S3.2.p1.pic1.2.2.2.1.1.3.1">Therefore, Jason gave 8 lollipops to Denny.</span></span> <span class="ltx_p" id="S3.2.p1.pic1.2.2.2.1.1.4"><span class="ltx_text ltx_font_typewriter" id="S3.2.p1.pic1.2.2.2.1.1.4.1">####<br class="ltx_break">8 lollipops</span></span></span></foreignObject></g></g></svg>

By contrast, Chain-of-Draft prompting condenses the reasoning process into minimal, abstract representations. Here, the reasoning is distilled into a concise equation, focusing solely on the essential mathematical operation required to arrive at the solution. By abstracting away irrelevant contextual details, CoD significantly reduces the token count while maintaining transparency and correctness.

<svg class="ltx_picture" height="126.58" id="S3.3.p1.pic1" overflow="visible" version="1.1" width="270"><g fill="#000000" stroke="#000000" stroke-width="0.4pt" transform="translate(0,126.58) matrix(1 0 0 -1 0 0)"><g fill="#BFBFBF" fill-opacity="1.0"><path d="M 0 5.91 L 0 120.68 C 0 123.94 2.64 126.58 5.91 126.58 L 264.09 126.58 C 267.35 126.58 270 123.94 270 120.68 L 270 5.91 C 270 2.64 267.35 0 264.09 0 L 5.91 0 C 2.64 0 0 2.64 0 5.91 Z"></path></g><g fill="#F2F2F2" fill-opacity="1.0"><path d="M 1.97 5.91 L 1.97 113.04 L 268.03 113.04 L 268.03 5.91 C 268.03 3.73 266.27 1.97 264.09 1.97 L 5.91 1.97 C 3.73 1.97 1.97 3.73 1.97 5.91 Z"></path></g><g fill-opacity="1.0" transform="matrix(1.0 0.0 0.0 1.0 17.72 115.01)"><foreignObject color="#FFFFFF" height="9.61" overflow="visible" transform="matrix(1 0 0 -1 0 16.6)" width="234.57"><span class="ltx_inline-block ltx_minipage ltx_align_bottom" id="S3.3.p1.pic1.1.1.1.1.1"><span class="ltx_p" id="S3.3.p1.pic1.1.1.1.1.1.1"><span class="ltx_text ltx_font_typewriter" id="S3.3.p1.pic1.1.1.1.1.1.1.1">Chain-of-Draft</span></span> </span></foreignObject></g><g fill-opacity="1.0" transform="matrix(1.0 0.0 0.0 1.0 17.72 9.84)"><foreignObject color="#000000" height="95.32" overflow="visible" transform="matrix(1 0 0 -1 0 16.6)" width="234.57"><span class="ltx_inline-block ltx_minipage ltx_align_bottom" id="S3.3.p1.pic1.2.2.2.1.1"><span class="ltx_p" id="S3.3.p1.pic1.2.2.2.1.1.1"><span class="ltx_text ltx_font_typewriter" id="S3.3.p1.pic1.2.2.2.1.1.1.1">Q: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?<br class="ltx_break">A: 20 - x = 12; x = 20 - 12 = 8. #### 8</span></span></span></foreignObject></g></g></svg>

## 4 Experiments

In empirical experiments, we follow the original CoT paper [^22] to evaluate on 3 categories of tasks: arithmetic reasoning, commonsense reasoning, and symbolic reasoning. We pick representative tasks where original CoT significantly improves the accuracy over the baseline without reasoning. In particular, we pick GSM8k [^7] for arithmetic reasoning; date understanding and sports understanding from BIG-bench [^1] for commonsense reasoning; and coin flip tasks introduced in the CoT paper [^22] for symbolic reasoning.

### 4.1 Experimental Setup

We compare three different prompt strategies: CoT, CoD, and Standard prompting as a baseline.

Standard prompting. we use standard few-shot prompting [^3], where the model is given input-output pairs as in-context examples. LLMs are asked to directly return the final answer, without any reasoning or explanation.

Chain-of-Thought. We follow the exact few-shot examples provided in the appendix of the CoT paper with the exception of having the final answer after four hashtags (####) for a more stable answer extraction.

Chain-of-Draft. In CoD, we also asked the model to think step by step. However, the model is asked to limit each reasoning step to five words at most. Note that we do not enforce such limitation in any way, it is just a general guideline to promte short reasoning steps. For each few-shot example, we also include the Chain of Draft written manually by the authors.

The complete system prompt for each prompting strategy is shown below.

<svg class="ltx_picture" height="76.4" id="S4.SS1.1.p1.pic1" overflow="visible" version="1.1" width="270"><g fill="#000000" stroke="#000000" stroke-width="0.4pt" transform="translate(0,76.4) matrix(1 0 0 -1 0 0)"><g fill="#BFBFBF" fill-opacity="1.0"><path d="M 0 5.91 L 0 70.5 C 0 73.76 2.64 76.4 5.91 76.4 L 264.09 76.4 C 267.35 76.4 270 73.76 270 70.5 L 270 5.91 C 270 2.64 267.35 0 264.09 0 L 5.91 0 C 2.64 0 0 2.64 0 5.91 Z"></path></g><g fill="#F2F2F2" fill-opacity="1.0"><path d="M 1.97 5.91 L 1.97 62.86 L 268.03 62.86 L 268.03 5.91 C 268.03 3.73 266.27 1.97 264.09 1.97 L 5.91 1.97 C 3.73 1.97 1.97 3.73 1.97 5.91 Z"></path></g><g fill-opacity="1.0" transform="matrix(1.0 0.0 0.0 1.0 17.72 64.83)"><foreignObject color="#FFFFFF" height="9.61" overflow="visible" transform="matrix(1 0 0 -1 0 16.6)" width="234.57"><span class="ltx_inline-block ltx_minipage ltx_align_bottom" id="S4.SS1.1.p1.pic1.1.1.1.1.1"><span class="ltx_p" id="S4.SS1.1.p1.pic1.1.1.1.1.1.1"><span class="ltx_text ltx_font_typewriter" id="S4.SS1.1.p1.pic1.1.1.1.1.1.1.1">Standard</span></span> </span></foreignObject></g><g fill-opacity="1.0" transform="matrix(1.0 0.0 0.0 1.0 17.72 9.84)"><foreignObject color="#000000" height="45.14" overflow="visible" transform="matrix(1 0 0 -1 0 16.6)" width="234.57"><span class="ltx_inline-block ltx_minipage ltx_align_bottom" id="S4.SS1.1.p1.pic1.2.2.2.1.1"><span class="ltx_p" id="S4.SS1.1.p1.pic1.2.2.2.1.1.1"><span class="ltx_text ltx_font_typewriter" id="S4.SS1.1.p1.pic1.2.2.2.1.1.1.1">Answer the question directly. Do not return any preamble, explanation, or reasoning.</span></span></span></foreignObject></g></g></svg>

<svg class="ltx_picture" height="96.07" id="S4.SS1.2.p2.pic1" overflow="visible" version="1.1" width="270"><g fill="#000000" stroke="#000000" stroke-width="0.4pt" transform="translate(0,96.07) matrix(1 0 0 -1 0 0)"><g fill="#BFBFBF" fill-opacity="1.0"><path d="M 0 5.91 L 0 90.16 C 0 93.42 2.64 96.07 5.91 96.07 L 264.09 96.07 C 267.35 96.07 270 93.42 270 90.16 L 270 5.91 C 270 2.64 267.35 0 264.09 0 L 5.91 0 C 2.64 0 0 2.64 0 5.91 Z"></path></g><g fill="#F2F2F2" fill-opacity="1.0"><path d="M 1.97 5.91 L 1.97 79.83 L 268.03 79.83 L 268.03 5.91 C 268.03 3.73 266.27 1.97 264.09 1.97 L 5.91 1.97 C 3.73 1.97 1.97 3.73 1.97 5.91 Z"></path></g><g fill-opacity="1.0" transform="matrix(1.0 0.0 0.0 1.0 17.72 81.8)"><foreignObject color="#FFFFFF" height="12.3" overflow="visible" transform="matrix(1 0 0 -1 0 16.6)" width="234.57"><span class="ltx_inline-block ltx_minipage ltx_align_bottom" id="S4.SS1.2.p2.pic1.1.1.1.1.1"><span class="ltx_p" id="S4.SS1.2.p2.pic1.1.1.1.1.1.1"><span class="ltx_text ltx_font_typewriter" id="S4.SS1.2.p2.pic1.1.1.1.1.1.1.1">Chain-of-Thought</span></span> </span></foreignObject></g><g fill-opacity="1.0" transform="matrix(1.0 0.0 0.0 1.0 17.72 9.84)"><foreignObject color="#000000" height="62.11" overflow="visible" transform="matrix(1 0 0 -1 0 16.6)" width="234.57"><span class="ltx_inline-block ltx_minipage ltx_align_bottom" id="S4.SS1.2.p2.pic1.2.2.2.1.1"><span class="ltx_p" id="S4.SS1.2.p2.pic1.2.2.2.1.1.1"><span class="ltx_text ltx_font_typewriter" id="S4.SS1.2.p2.pic1.2.2.2.1.1.1.1">Think step by step to answer the following question. Return the answer at the end of the response after a separator ####.</span></span></span></foreignObject></g></g></svg>

<svg class="ltx_picture" height="109.98" id="S4.SS1.3.p3.pic1" overflow="visible" version="1.1" width="270"><g fill="#000000" stroke="#000000" stroke-width="0.4pt" transform="translate(0,109.98) matrix(1 0 0 -1 0 0)"><g fill="#BFBFBF" fill-opacity="1.0"><path d="M 0 5.91 L 0 104.07 C 0 107.34 2.64 109.98 5.91 109.98 L 264.09 109.98 C 267.35 109.98 270 107.34 270 104.07 L 270 5.91 C 270 2.64 267.35 0 264.09 0 L 5.91 0 C 2.64 0 0 2.64 0 5.91 Z"></path></g><g fill="#F2F2F2" fill-opacity="1.0"><path d="M 1.97 5.91 L 1.97 96.43 L 268.03 96.43 L 268.03 5.91 C 268.03 3.73 266.27 1.97 264.09 1.97 L 5.91 1.97 C 3.73 1.97 1.97 3.73 1.97 5.91 Z"></path></g><g fill-opacity="1.0" transform="matrix(1.0 0.0 0.0 1.0 17.72 98.4)"><foreignObject color="#FFFFFF" height="9.61" overflow="visible" transform="matrix(1 0 0 -1 0 16.6)" width="234.57"><span class="ltx_inline-block ltx_minipage ltx_align_bottom" id="S4.SS1.3.p3.pic1.1.1.1.1.1"><span class="ltx_p" id="S4.SS1.3.p3.pic1.1.1.1.1.1.1"><span class="ltx_text ltx_font_typewriter" id="S4.SS1.3.p3.pic1.1.1.1.1.1.1.1">Chain-of-Draft</span></span> </span></foreignObject></g><g fill-opacity="1.0" transform="matrix(1.0 0.0 0.0 1.0 17.72 9.84)"><foreignObject color="#000000" height="78.72" overflow="visible" transform="matrix(1 0 0 -1 0 16.6)" width="234.57"><span class="ltx_inline-block ltx_minipage ltx_align_bottom" id="S4.SS1.3.p3.pic1.2.2.2.1.1"><span class="ltx_p" id="S4.SS1.3.p3.pic1.2.2.2.1.1.1"><span class="ltx_text ltx_font_typewriter" id="S4.SS1.3.p3.pic1.2.2.2.1.1.1.1">Think step by step, but only keep a minimum draft for each thinking step, with 5 words at most. Return the answer at the end of the response after a separator ####.</span></span></span></foreignObject></g></g></svg>

We evaluated each task with two of the most popular flagship models: GPT-4o (gpt-4o-2024-08-06) from OpenAI and Claude 3.5 Sonnet (claude-3-5-sonnet-20240620) from Anthropic.

### 4.2 Arithmetic Reasoning

We first consider math problems that measure the arithmetic reasoning capabilities of LLMs. GSM8k [^7] has emerged as the benchmark of choice for evaluating arithmetic reasoning in language models, providing a comprehensive dataset of 8,500 diverse grade-school-level mathematical problems. Each problem is paired with a detailed step-by-step solution, emphasizing arithmetic, geometry, algebra, and logical reasoning skills.

The evaluation results are presented in Table [1](https://arxiv.org/html/2502.18600v2#S4.T1 "Table 1 ‣ 4.2 Arithmetic Reasoning ‣ 4 Experiments ‣ Chain of Draft: Thinking Faster by Writing Less"). The dataset poses significant challenges for both GPT-4o and Claude 3.5 Sonnet when using standard prompting, yielding accuracies of 53.3% and 64.6%, respectively. However, with the application of the CoT, both models surpass 95% accuracy, albeit at the expense of generating approximately 200 tokens per response. In contrast, CoD achieves an accuracy of 91% for both models while requiring only about 40 tokens per response, thereby reducing the average output token count by 80% and cutting the average latency by 76.2% and 48.4%, respectively.

Table 1: GSM8K evaluation results.

### 4.3 Commonsense Reasoning

We evaluate the tasks of date understanding and sports understanding from BIG-bench to demonstrate the effectiveness of CoD in common sense reasoning. For consistency, we use the same system prompts as those employed in the arithmetic reasoning evaluation.

The evaluation results, presented in Table [2](https://arxiv.org/html/2502.18600v2#S4.T2 "Table 2 ‣ 4.3 Commonsense Reasoning ‣ 4 Experiments ‣ Chain of Draft: Thinking Faster by Writing Less"), show that CoD significantly reduces both latency and cost by generating considerably fewer tokens in responses compared to CoT. Additionally, CoD outperforms CoT in accuracy in various cases. Notably, chain-of-thought prompting leads to excessively verbose responses for Claude 3.5 Sonnet, especially in the sports understanding task, where CoD reduces the average output tokens from 189.4 to 14.3 — a 92.4% reduction.

Table 2: Date understanding evaluation results.

Table 3: Sports understanding evaluation results.

### 4.4 Symbolic Reasoning

The original CoT paper [^22] introduces the task of coin flipping, where the LLMs are asked to predict which side is up after a sequence of coin flip actions. Since the exact dataset is not published, we synthesize a test set of 250 examples following the same design. Specifically, we randomly chose 4 out of the top 1000 first names in the US region according to NameDataset [^18] and randomly decided to flip the coin or not for each name. An example of the evaluation data is shown below.

<svg class="ltx_picture" height="95.56" id="S4.SS4.1.p1.pic1" overflow="visible" version="1.1" width="270"><g fill="#000000" stroke="#000000" stroke-width="0.4pt" transform="translate(0,95.56) matrix(1 0 0 -1 0 0)"><g fill="#BFBFBF" fill-opacity="1.0"><path d="M 0 5.91 L 0 89.65 C 0 92.91 2.64 95.56 5.91 95.56 L 264.09 95.56 C 267.35 95.56 270 92.91 270 89.65 L 270 5.91 C 270 2.64 267.35 0 264.09 0 L 5.91 0 C 2.64 0 0 2.64 0 5.91 Z"></path></g><g fill="#F2F2F2" fill-opacity="1.0"><path d="M 1.97 5.91 L 1.97 89.65 C 1.97 91.83 3.73 93.59 5.91 93.59 L 264.09 93.59 C 266.27 93.59 268.03 91.83 268.03 89.65 L 268.03 5.91 C 268.03 3.73 266.27 1.97 264.09 1.97 L 5.91 1.97 C 3.73 1.97 1.97 3.73 1.97 5.91 Z"></path></g><g fill-opacity="1.0" transform="matrix(1.0 0.0 0.0 1.0 17.72 9.84)"><foreignObject color="#000000" height="75.87" overflow="visible" transform="matrix(1 0 0 -1 0 16.6)" width="234.57"><span class="ltx_inline-block ltx_minipage ltx_align_bottom" id="S4.SS4.1.p1.pic1.1.1.1.1.1"><span class="ltx_p" id="S4.SS4.1.p1.pic1.1.1.1.1.1.1"><span class="ltx_text ltx_font_typewriter" id="S4.SS4.1.p1.pic1.1.1.1.1.1.1.1">Q: A coin is heads up. Robyn flips the coin. Peggy flips the coin. Grant flips the coin. Vanessa does not flip the coin. Is the coin still heads up?<br class="ltx_break">A: No.</span></span></span></foreignObject></g></g></svg>

The evaluation results for GPT-4o and Claude 3.5 Sonnet are shown in Table [4](https://arxiv.org/html/2502.18600v2#S4.T4 "Table 4 ‣ 4.4 Symbolic Reasoning ‣ 4 Experiments ‣ Chain of Draft: Thinking Faster by Writing Less"). They achieve 73.2% and 85.2% with standard prompting, respectively. However, both models reach a perfect 100% accuracy with CoT and CoD. Again, CoD demonstrates significant reduction of tokens compared to CoT, from 68% for GPT-4o to 86% for Claude 3.5 Sonnet.

Table 4: Coin flip evaluation results.

### 4.5 Limitaitons of CoD

Inconsistency Without Few-shot Examples

We evaluated the performance of CoD under zero-shot setting, where no few-shot examples were provided. The results, presented in Table [5](https://arxiv.org/html/2502.18600v2#S4.T5 "Table 5 ‣ 4.5 Limitaitons of CoD ‣ 4 Experiments ‣ Chain of Draft: Thinking Faster by Writing Less"), indicate a significant decline in CoD’s effectiveness. Notably, for Claude 3.5 Sonnet, CoD improved performance over direct answering by only 3.6%. Additionally, the token savings achieved by CoD are less significant compared to few-shot setting.

We hypothesize that this limitation arises due to the scarcity or absence of CoD-style reasoning patterns in the training data of large language models, making it a challenging task to generate concise and insightful “drafts” without guidance from few-shot examples.

Table 5: Zero-shot GSM8K evaluation results.

Reduced Performance on Small Models

We tested CoD on several small language models with fewer than 3B parameters, including Qwen2.5 1.5B/3B instruct [^23], Llama 3.2 3B instruct [^8], and our in-house Zoom SLM 2.3B model [^28]. While CoD effectively reduces the number of tokens required per response and improves accuracy over direct answer, its performance gap compared to CoT is more pronounced in these models.

Similar to the zero-shot setting, we suspect this is due to the absence of CoD-style data in the training process. We anticipate that fine-tuning these models with additional CoD-formatted data could significantly enhance their reasoning accuracy with CoD.

Table 6: GSM8K evaluation results on small language models.

## 5 Discussion

The latency issue has often been overlooked in studies of the reasoning capabilities of LLMs. However, it is crucial for lots of real-time applications to have low latency while maintaining high-quality responses. In this work, we propose Chain of Draft (CoD), a novel approach that substantially reduces the latency required for reasoning while achieving comparable or even superior accuracy compared to standard Chain-of-Thought prompting strategies. Unlike traditional methods that often involve lengthy reasoning steps, CoD leverages concise reasoning drafts to speed up response generation without sacrificing correctness.

Additionally, CoD offers significant cost advantages. By compacting the reasoning steps, it reduces the number of input tokens required for few-shot prompting and shortens the output token length, directly lowering computational cost. This token efficiency makes CoD especially appealing in cost-sensitive scenarios, such as large-scale deployments of LLMs or applications with strict budget constraints.

CoD demonstrates that effective reasoning in LLMs does not necessarily require lengthy outputs, offering an alternative approach where reasoning depth is maintained with minimal verbosity. Future work could explore combining CoD with other latency-reducing methods, such as adaptive parallel reasoning or multi-pass validation, to further optimize performance across different application domains. In addition, the principles behind the compact reasoning of CoD could inspire new strategies to improve reasoning models by training with compact reasoning data, while maintaining interpretability and efficiency in LLMs, helping bridge the gap between research-driven improvements in reasoning and the practical demands of real world systems.

## References

[^1]: BIG bench authors. 2023. [Beyond the imitation game: Quantifying and extrapolating the capabilities of language models](https://openreview.net/forum?id=uyTL5Bvosj). *Transactions on Machine Learning Research*.

[^2]: Maciej Besta, Nils Blach, Ales Kubicek, Robert Gerstenberger, Michal Podstawski, Lukas Gianinazzi, Joanna Gajda, Tomasz Lehmann, Hubert Niewiadomski, Piotr Nyczyk, et al. 2024. Graph of thoughts: Solving elaborate problems with large language models. In *Proceedings of the AAAI Conference on Artificial Intelligence*, volume 38, pages 17682–17690.

[^3]: Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel Ziegler, Jeffrey Wu, Clemens Winter, Chris Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. 2020. [Language models are few-shot learners](https://proceedings.neurips.cc/paper_files/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf). In *Advances in Neural Information Processing Systems*, volume 33, pages 1877–1901. Curran Associates, Inc.

[^4]: Sijia Chen, Baochun Li, and Di Niu. 2024a. Boosting of thoughts: Trial-and-error problem solving with large language models. *arXiv preprint arXiv:2402.11140*.

[^5]: Xingyu Chen, Jiahao Xu, Tian Liang, Zhiwei He, Jianhui Pang, Dian Yu, Linfeng Song, Qiuzhi Liu, Mengfei Zhou, Zhuosheng Zhang, et al. 2024b. Do not think that much for 2+ 3=? on the overthinking of o1-like llms. *arXiv preprint arXiv:2412.21187*.

[^6]: Cheng-Han Chiang and Hung-yi Lee. 2024. Over-reasoning and redundant calculation of large language models. *arXiv preprint arXiv:2401.11467*.

[^7]: Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John Schulman. 2021. Training verifiers to solve math word problems. *arXiv preprint arXiv:2110.14168*.

[^8]: Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan, et al. 2024. The llama 3 herd of models. *arXiv preprint arXiv:2407.21783*.

[^9]: Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al. 2025. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. *arXiv preprint arXiv:2501.12948*.

[^10]: Tingxu Han, Chunrong Fang, Shiyu Zhao, Shiqing Ma, Zhenyu Chen, and Zhenting Wang. 2024. Token-budget-aware llm reasoning. *arXiv preprint arXiv:2412.18547*.

[^11]: Shibo Hao, Sainbayar Sukhbaatar, DiJia Su, Xian Li, Zhiting Hu, Jason Weston, and Yuandong Tian. 2024. Training large language models to reason in a continuous latent space. *arXiv preprint arXiv:2412.06769*.

[^12]: Song Jiang, Zahra Shakeri, Aaron Chan, Maziar Sanjabi, Hamed Firooz, Yinglong Xia, Bugra Akyildiz, Yizhou Sun, Jinchao Li, Qifan Wang, et al. 2023. Resprompt: Residual connection prompting advances multi-step reasoning in large language models. *arXiv preprint arXiv:2310.04743*.

[^13]: Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa. 2022. Large language models are zero-shot reasoners. *Advances in neural information processing systems*, 35:22199–22213.

[^14]: Bin Lei, Chunhua Liao, Caiwen Ding, et al. 2023. Boosting logical reasoning in large language models through a new framework: The graph of thought. *arXiv preprint arXiv:2308.08614*.

[^15]: Sania Nayab, Giulio Rossolini, Giorgio Buttazzo, Nicolamaria Manes, and Fabrizio Giacomelli. 2024. Concise thoughts: Impact of output length on llm reasoning and cost. *arXiv preprint arXiv:2407.19825*.

[^16]: Xuefei Ning, Zinan Lin, Zixuan Zhou, Zifu Wang, Huazhong Yang, and Yu Wang. 2023. Skeleton-of-thought: Large language models can do parallel decoding. *Proceedings ENLSP-III*.

[^17]: OpenAI. 2024. [Openai o1 system card](https://openai.com/index/openai-o1-system-card/). Accessed: 2024-12-01.

[^18]: Philippe Remy. 2021. Name dataset. [https://github.com/philipperemy/name-dataset](https://github.com/philipperemy/name-dataset).

[^19]: Qwen Team. 2024. [Qwq: Reflect deeply on the boundaries of the unknown](https://qwenlm.github.io/blog/qwq-32b-preview/).

[^20]: Junlin Wang, Siddhartha Jain, Dejiao Zhang, Baishakhi Ray, Varun Kumar, and Ben Athiwaratkun. 2024. Reasoning in token economies: Budget-aware evaluation of llm reasoning strategies. *arXiv preprint arXiv:2406.06461*.

[^21]: Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou. 2022. Self-consistency improves chain of thought reasoning in language models. *arXiv preprint arXiv:2203.11171*.

[^22]: Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, brian ichter, Fei Xia, Ed Chi, Quoc V Le, and Denny Zhou. 2022. [Chain-of-thought prompting elicits reasoning in large language models](https://proceedings.neurips.cc/paper_files/paper/2022/file/9d5609613524ecf4f15af0f7b31abca4-Paper-Conference.pdf). In *Advances in Neural Information Processing Systems*, volume 35, pages 24824–24837. Curran Associates, Inc.

[^23]: An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan Li, Dayiheng Liu, Fei Huang, Haoran Wei, et al. 2024. Qwen2. 5 technical report. *arXiv preprint arXiv:2412.15115*.

[^24]: Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Tom Griffiths, Yuan Cao, and Karthik Narasimhan. 2024. Tree of thoughts: Deliberate problem solving with large language models. *Advances in Neural Information Processing Systems*, 36.

[^25]: Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. 2022. React: Synergizing reasoning and acting in language models. *arXiv preprint arXiv:2210.03629*.

[^26]: Junchi Yu, Ran He, and Rex Ying. 2023. Thought propagation: An analogical approach to complex reasoning with large language models. *arXiv preprint arXiv:2310.03965*.

[^27]: Jun Zhang, Jue Wang, Huan Li, Lidan Shou, Ke Chen, Gang Chen, and Sharad Mehrotra. 2023. Draft & verify: Lossless large language model acceleration via self-speculative decoding. *arXiv preprint arXiv:2309.08168*.

[^28]: Zoom. 2025. How we’re preparing for the next era of AI. [https://www.zoom.com/en/blog/what-is-agentic-ai](https://www.zoom.com/en/blog/what-is-agentic-ai).