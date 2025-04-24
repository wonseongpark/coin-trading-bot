def get_dynamic_allocation(pnls):
    min_weight = 0.05
    adjusted = {k: max(v, 0.01) for k, v in pnls.items()}
    total = sum(adjusted.values())
    raw_weights = {k: adjusted[k] / total for k in adjusted}

    final_weights = {}
    for k in raw_weights:
        final_weights[k] = max(raw_weights[k], min_weight)

    sum_weights = sum(final_weights.values())
    normalized_weights = {k: v / sum_weights for k, v in final_weights.items()}
    return normalized_weights
