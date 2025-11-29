# RAG Data Generation and Ingestion Pipeline

This document describes the purpose of `synthetic_data_gen.py` and the planned pipeline that takes generated domain corpora from local output through S3 into Amazon Bedrock Knowledge Bases backed by OpenSearch Serverless vectors.

## Purpose of `synthetic_data_gen.py`

- Generates finance- and economics-focused synthetic corpora in four domains: monetary policy summaries, economic indicators, regulatory changes, and policy decisions (central banking).
- Produces chronologically coherent, narrative-rich text files suitable for Retrieval Augmented Generation (RAG) workloads.
- Allows configurable record counts and historical span to scale dataset size for experimentation.
- Creates a single output directory `financial_intelligence_data/` containing one text file per domain, ready for upload.

## End-to-End Pipeline (pencil sketch)

```
Developer laptop
    |
    | 1) Run synthetic_data_gen.py
    v
financial_intelligence_data/ (local text corpora)
    |
    | 2) Sync/upload
    v
S3 bucket (raw domain corpora, versioned)
    |
    | 3) Bedrock Knowledge Base ingestion job
    v
OpenSearch Serverless vector index (per-domain collections)
    |
    | 4) Bedrock KB runtime
    v
EconFlux agent tools -> grounded answers
```

## Pipeline Stages

1) **Generate**  
   - Run `python src/rag/synthetic_data_gen.py --records <N> --years <Y>`  
   - Output: `financial_intelligence_data/{monetary_policy_summaries,economic_indicators,regulatory_changes,policy_decisions}.txt`

2) **Stage & Validate**  
   - Sanity-check counts, date ranges, and spot-read samples for coherence.  
   - Optional: run a lint step to confirm UTF-8 encoding and file sizes before upload.

3) **Upload to S3**  
   - Choose an S3 bucket/prefix per environment (e.g., `s3://econflux-rag-data/dev/`).  
   - Keep domain files separated by prefix to mirror KB domains.  
   - Enable versioning to audit and roll back corpus changes.

4) **Ingest into Bedrock Knowledge Bases (OpenSearch vectors)**  
   - Create four Bedrock Knowledge Bases, each mapped to an OpenSearch Serverless collection:  
     - `kb_monetary_policy_summaries`  
     - `kb_economic_indicators`  
     - `kb_regulatory_changes`  
     - `kb_policy_decisions`  
   - Configure ingestion from the S3 prefixes above. Bedrock handles chunking, embeddings, and vector storage in OpenSearch.  
   - Confirm ingestion metrics (document counts, chunk counts, errors) after each load.

5) **Consume from the Agent**  
   - Implement four RAG tools (one per domain) that query the corresponding KB.  
   - Tools will pass retrieved chunks into the model context so EconFlux can ground answers for central banking and economist workflows.  
   - Add retrieval logging/telemetry to monitor hit rates and relevance.

## Operational Notes

- **Schema/format**: Keep the text files as plain UTF-8; avoid exotic formatting. If you later switch to JSONL, ensure the KB ingestion config matches.  
- **Refresh cadence**: Regenerate and reingest when adding new narratives or adjusting parameters (`--records`, `--years`).  
- **Quality controls**: Maintain a small “golden set” snapshot to compare against newly generated corpora for drift checks.  
- **Security**: Use least-privilege IAM for S3 access and Bedrock KB ingestion roles; bucket should deny public access.  
- **Cost awareness**: OpenSearch vector storage scales with chunk count; tune chunk size and deduplicate corpora to control footprint.
