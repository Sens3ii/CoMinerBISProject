import re


def optimize_text(text, entity):
    print("[OPTIMIZATION] Optimization of text")
    pattern = '.{50}' + entity + '.{50}'
    print(f"========================== {pattern}")
    optimized_text = re.findall(pattern, text)
    optimized_text = ' '.join(optimized_text)
    return optimized_text


