# Cost Calculation Breakdown - Self-Hosted with OpenAI API

## Overview

This document provides a cost estimation for the ECSS Knowledge Graph project assuming a **self-hosted Morphik instance** that makes direct API calls to OpenAI. This model is different from using a Morphik managed cloud plan.

Costs are calculated based on the specific models defined in `morphik.toml` and the public [OpenAI API pricing](https://platform.openai.com/docs/pricing).

## 1. Key Assumptions

| Metric | Value | Justification |
|---|---|---|
| **Total Documents** | 5 | Initial batch for analysis. |
| **Avg. Pages per Doc** | 80 | Conservative estimate for ECSS standards. |
| **Total Pages** | 400 | 5 docs × 80 pages/doc. |
| **Avg. Tokens per Page** | 1,000 | Standard estimate for technical text. |
| **Total Content Tokens** | 400,000 | 400 pages × 1,000 tokens/page. |
| **Avg. Images per Doc** | 10 | Estimate for diagrams and tables. |
| **Total Images** | 50 | 5 docs × 10 images/doc. |
| **Extraction Rules** | 6 | `ECSSStandard`, `ECSSSection`, etc. |
| **Rules Batch Size** | 4,096 tokens | As per `morphik.toml`. |

## 2. OpenAI Model Pricing

| Model | Input Cost (per 1M tokens) | Output Cost (per 1M tokens) |
|---|---|---|
| **GPT-4o** | $5.00 | $15.00 |
| **GPT-4o-mini** | $0.15 | $0.60 |
| **text-embedding-3-large** | $0.13 | N/A |

## 3. Detailed Cost Breakdown (5 Documents)

The total cost is the sum of four distinct processing steps:

### A. Vector Embeddings
- **Model**: `text-embedding-3-large`
- **Tokens**: 400,000
- **Calculation**: `(400,000 / 1,000,000) * $0.13`
- **Cost**: **$0.05**

### B. Contextual Chunking
- **Model**: `gpt-4o-mini`
- **Input Tokens**: ~400,000 (Processes all content)
- **Output Tokens**: ~40,000 (Estimated 10% of input)
- **Calculation**: `(0.4M * $0.15) + (0.04M * $0.60)`
- **Cost**: **$0.08**

### C. Rules & Graph Extraction (Most Expensive Step)
This step is costly because it makes an API call to `gpt-4o` for **each rule** applied to **each batch** of a document.
- **Batches per Doc**: `(80,000 tokens/doc) / 4,096 tokens/batch` ≈ 20 batches
- **API Calls per Doc**: `20 batches * 6 rules` = 120 calls
- **Total Input Tokens**: `5 docs * 120 calls/doc * 4,096 tokens/call` ≈ 2.46M tokens
- **Total Output Tokens**: (Estimated 10% of input) ≈ 0.25M tokens
- **Input Cost**: `2.46 * $5.00` = $12.30
- **Output Cost**: `0.25 * $15.00` = $3.75
- **Cost**: **$16.05**

### D. Vision Processing (Images & Diagrams)
- **Model**: `gpt-4o`
- **Total Images**: 50
- **Input Tokens**: `50 images * (765 tokens/image + 100 prompt tokens)` ≈ 43,250 tokens
- **Output Tokens**: `50 images * 100 caption tokens` = 5,000 tokens
- **Input Cost**: `(43,250 / 1,000,000) * $5.00` = $0.22
- **Output Cost**: `(5,000 / 1,000,000) * $15.00` = $0.08
- **Cost**: **$0.30**

---

## 4. Total Estimated Cost

| Component | Calculation | Cost (5 Docs) |
|---|---|---|
| **A. Vector Embeddings** | `(0.4M / 1M) * $0.13` | **$0.05** |
| **B. Contextual Chunking** | `(0.4M * $0.15) + (0.04M * $0.60)` | **$0.08** |
| **C. Rules & Graph Extraction**| `(2.46M * $5.00) + (0.25M * $15.00)` | **$16.05** |
| **D. Vision Processing** | `(0.043M * $5.00) + (0.005M * $15.00)` | **$0.30** |
| **Grand Total** | | **~$16.48** |

## 5. Scaling Analysis

| Documents | Total Tokens | Est. Rules/Graph Cost | Total Estimated Cost |
|---|---|---|---|
| **5** | 0.4M | $16.05 | **~$16.48** |
| **50** | 4.0M | $160.50 | **~$164.80** |

## 6. Conclusion

For a self-hosted instance, the vast majority of the cost (**~97%**) comes from using `gpt-4o` for the rules-based metadata and knowledge graph extraction. This explains why a missing `OPENAI_API_KEY` would cause the process to fail silently—it was unable to make the large number of required API calls. The cost is directly proportional to the number of documents and the number of extraction rules applied.
