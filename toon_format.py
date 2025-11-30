import json
from toon_python import encode

# optional: use tiktoken if installed for real token counts, otherwise fall back to a simple estimate
try:
    import tiktoken

    def _count_tokens_with_tiktoken(s: str, model: str = "gpt5-mini") -> int:
        try:
            enc = tiktoken.encoding_for_model(model)
        except Exception:
            enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(s))
except Exception:
    _count_tokens_with_tiktoken = None

def count_tokens(s: str, model: str = "gpt5-mini") -> int:
    if _count_tokens_with_tiktoken:
        return _count_tokens_with_tiktoken(s, model)
    # fallback heuristic
    return max(1, len(s) // 4)

def compare_formats(data) -> str:
    json_str = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    toon_str = encode(data)
    tokens_json = count_tokens(json_str)
    tokens_toon = count_tokens(toon_str)
    return (
        "Format      Tokens    Size (chars)\n"
        f"JSON         {tokens_json:<8} {len(json_str):<12}\n"
        f"TOON         {tokens_toon:<8} {len(toon_str):<12}"
    )

def estimate_savings(data) -> dict:
    json_str = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    toon_str = encode(data)
    tokens_json = count_tokens(json_str)
    tokens_toon = count_tokens(toon_str)
    savings = tokens_json - tokens_toon
    percent = (savings / tokens_json * 100) if tokens_json else 0.0
    return {
        "tokens_json": tokens_json,
        "tokens_toon": tokens_toon,
        "savings": savings,
        "savings_percent": percent,
    }