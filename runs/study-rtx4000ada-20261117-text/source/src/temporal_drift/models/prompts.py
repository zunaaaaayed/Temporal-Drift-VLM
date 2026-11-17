def build_prompts(cfg: dict) -> list[dict]:
    e, p = cfg["experiment"], cfg["prompts"]
    records = []
    for lang in e["languages"]:
        for concept in sorted(e["concepts"]):
            name = p["CONCEPT_NAMES"][lang][concept]
            for b in [*e["temporal_bins"], "neutral"]:
                templates = (
                    p["NEUTRAL_TMPLS"][lang] if b == "neutral" else p["TEMPORAL_TMPLS"][lang]
                )
                period = "" if b == "neutral" else p["PERIOD_LABEL"][b][lang]
                for i, template in enumerate(templates):
                    records.append(
                        {
                            "prompt_id": f"{lang}/{concept}/{b}/{i}",
                            "language": lang,
                            "concept": concept,
                            "temp_bin": b,
                            "paraphrase": i,
                            "text": template.format(concept=name, period=period),
                        }
                    )
    return records
