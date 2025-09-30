import os
import streamlit as st
from openai import OpenAI
from datasets import Dataset
from ragas.metrics import summarization_score
from ragas import evaluate


def evaluate_summarization(source_text: str, generated_summary: str):
    """
    Evaluates a generated summary using Ragas' SummarizationScore metric.
    """
    # Create a Dataset object, which Ragas uses for evaluation.
    # The 'contexts' key is used for the source text.
    data = {
        'contexts': [[source_text]],
        'answer': [generated_summary],
        "reference_contexts": [[source_text]]  # Optional, but can help with evaluation
    }
    dataset = Dataset.from_dict(data)
    #print(dataset)

    # Run the evaluation with the summarization_score metric
    eval_results = evaluate(
        dataset,
        metrics=[summarization_score],
    )
    
    # Print the results in a readable format
    print(eval_results)
    
    print("\nDetailed Evaluation Results:")
    for result in eval_results.to_pandas().itertuples():
        st.write(f"Evaluation for Text: '{source_text[:50]}...'")
        st.write(f"Generated Summary: {result.response}")
        st.write("-" * 20)
        st.write(f"Summarization Score: {result.summary_score:.4f}")
        # Note: Ragas doesn't provide a reasoning breakdown for this metric
        # like DeepEval, so we can't print a reasoning string here.
        #print("\n")
        