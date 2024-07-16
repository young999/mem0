from mem0 import Memory

config = {
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "llama3",
        }
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text",
            "dims": 768,
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333,
        }
    },
    "collection_name": "mem0",
}

memory = Memory.from_config(config=config)

memory.add("I am planning a trip to Spain. Suggest some places to visit", user_id="deshraj1")

memory.get_all(user_id="deshraj1")
