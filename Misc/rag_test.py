import time

knowledge_base = {
    "doc_1": "Visakhapatnam is known as the Jewel of the East Coast and features major industrial corridors.",
    "doc_2": "Dual-stage RAG architectures use an initial retriever for fast candidate selection followed by a precision reranker.",
    "doc_3": "IIT Madras offers an online BS Degree in Data Science and Applications focusing on modern data pipelines.",
    "doc_4": "Vector embeddings capture semantic meaning, allowing dense retrieval to find context even when keywords differ.",
    "doc_5": "The commercial office building architecture required extensive civil engineering work before interior cabling could begin."
}

def query_expansion(query):
    query_lower = query.lower()
    expanded_terms = [query]
    
    if "data science" in query_lower or "iit" in query_lower:
        expanded_terms.append("analytics machine learning degree curriculum")
    elif "visakhapatnam" in query_lower:
        expanded_terms.append("port city industrial east coast")
        
    full_expanded_query = " ".join(expanded_terms)
    return full_expanded_query

def mock_retriever(query):
    query_tokens = set(w.lower() for w in query.split() if len(w) > 3)
    results = []
    for doc_id, text in knowledge_base.items():
        text_lower = text.lower()
        if any(token in text_lower for token in query_tokens):
            results.append((doc_id, text))
    return results[:4]

def mock_reranker(query, candidates):
    query_tokens = set(w.lower() for w in query.split() if len(w) > 3)
    scored = []
    
    for doc_id, text in candidates:
        text_lower = text.lower()
        matches = sum(1 for token in query_tokens if token in text_lower)
        score = matches / len(query_tokens) if query_tokens else 0.0
        
        # Domain specific boosting
        if "data science" in text_lower or "applications" in text_lower:
            score += 0.4
            
        scored.append((doc_id, text, round(score, 2)))
    
    scored.sort(key=lambda x: x[2], reverse=True)
    return scored

def mock_generator(query, final_results):
    # Stricter threshold test (increased from 0.4 to 0.5)
    if not final_results or final_results[0][2] < 0.5:
        return "[THRESHOLD REJECTION] Top score was too low. I could not find sufficiently relevant information to safely answer your query."
    
    top_doc_id, top_text, top_score = final_results[0]
    return f"Based on retrieved context ([{top_doc_id}] with score {top_score}): {top_text}"

if __name__ == "__main__":
    # Test with a brand new query!
    raw_query = "What does the IIT Madras program focus on?"
    print(f"Raw Query: {raw_query}\n")
    
    start_time = time.time()
    
    expanded_query = query_expansion(raw_query)
    print(f"Expanded Query: {expanded_query}\n")
    
    candidates = mock_retriever(expanded_query)
    print(f"Stage 1 Retrieved {len(candidates)} candidates.")
    
    final_results = mock_reranker(expanded_query, candidates)
    final_answer = mock_generator(raw_query, final_results)
    
    elapsed = (time.time() - start_time) * 1000
    
    print("\nFinal Reranked Results:")
    for rank, (doc_id, text, score) in enumerate(final_results, 1):
        print(f"  {rank}. [{doc_id}] Score: {score} -> {text}")
        
    print(f"\n--- Generated LLM Output ---\n{final_answer}")
    print(f"\nTotal Pipeline Execution time: {elapsed:.2f} ms")

