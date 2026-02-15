from pathlib import Path

# Project root 
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directory
DATA_DIR = BASE_DIR / "data"

# Raw Data files
STRATEGIC_DOCUMENT_PATH = DATA_DIR / "strategic_plan_commercial_bank.md"
ACTION_DOCUMENT_PATH = DATA_DIR / "action_plan_commercial_bank.md"

# Document Processor results
STRATEGIC_PLAN_PATH = DATA_DIR / "strategic_plan.json"
ACTION_PLAN_PATH = DATA_DIR / "action_plan.json"

# Embedding Analyzer results
EMBEDDING_ANALYZER_RESULTS_PATH = DATA_DIR / "embedding_analysis_results.json"

# Entity Extractor results
ENTITY_ANALYSIS_RESULTS_PATH = DATA_DIR / "entity_analysis_results.json"

# Scoring Engine results
FINAL_SYNCHRONIZATION_RESULTS_PATH = DATA_DIR / "final_synchronization_results.json"

# LLM Engine results
LLM_SYNCHRONIZATION_RESULTS_PATH = DATA_DIR / "llm_synchronization_results.json"

