# import json
# import os
# from pathlib import Path

# OUTPUT_FILE = "/home/harshchinchakar/WORK Files/HR Bot/Scores.json"

# # Define weights for weighted average
# WEIGHTS = {
#     "difficulty": 0.142857,
#     "novelty": 0.142857,
#     "skill_relevance": 0.142857,
#     "complexity": 0.142857,
#     "technical_depth": 0.142857,
#     "domain_relevance": 0.142857,
#     "execution_quality": 0.142857
# }

# def calculate_weighted_score(metrics: dict) -> float:
#     """Calculate weighted score for a single project."""
#     total_score = 0
#     total_weight = 0
#     for metric, weight in WEIGHTS.items():
#         if metric in metrics:
#             total_score += metrics[metric] * weight
#             total_weight += weight
#     return round(total_score / total_weight, 3) if total_weight > 0 else 0.0


# def process_resume(json_path: str):
#     """Process a single resume JSON and return candidate project aggregate score."""
#     if json_path.endswith("example_output.json"):
#         print(f"⏭️ Skipping reference file: {json_path}")
#         return None

#     with open(json_path, "r") as f:
#         data = json.load(f)

#     candidate_name = data.get("name", "Unknown")

#     projects = data.get("projects", [])
#     if not projects:
#         aggregate_score = 0.0
#     else:
#         project_scores = [calculate_weighted_score(p.get("metrics", {})) for p in projects]
#         aggregate_score = round(sum(project_scores) / len(project_scores), 3)

#     return {
#         "name": candidate_name,
#         "project_aggregate": aggregate_score
#     }


# def write_scores(results: list):
#     """Write all results into Scores.json"""
#     if os.path.exists(OUTPUT_FILE):
#         with open(OUTPUT_FILE, "r") as f:
#             try:
#                 scores_data = json.load(f)
#             except json.JSONDecodeError:
#                 scores_data = []
#     else:
#         scores_data = []

#     scores_data.extend(results)

#     with open(OUTPUT_FILE, "w") as f:
#         json.dump(scores_data, f, indent=4)


# def main(dir_path: str):
#     """Process all JSON resumes in the given directory."""
#     results = []
#     for json_file in Path(dir_path).glob("*.json"):
#         result = process_resume(str(json_file))
#         if result:
#             results.append(result)
#             print(f"✅ Processed {result['name']} | Project Aggregate: {result['project_aggregate']}")

#     if results:
#         write_scores(results)
#         print(f"\n📂 All results written to {OUTPUT_FILE}")
#     else:
#         print("⚠️ No valid resumes processed.")


# if __name__ == "__main__":
#     import argparse
#     parser = argparse.ArgumentParser(description="Calculate project aggregate scores from resumes in a directory")
#     parser.add_argument("dir_path", type=str, help="Path to directory with resume JSONs")
#     args = parser.parse_args()
#     main(args.dir_path)

##!/usr/bin/env python3
import json
from pathlib import Path

OUTPUT_FILE = Path("/home/keeda/HR BOT/Ranking/Scores.json")
PROCESSED_JSON_DIR = Path("/home/keeda/HR BOT/ProcessedJson")

# Define weights for weighted average
WEIGHTS = {
    "difficulty": 0.142857,
    "novelty": 0.142857,
    "skill_relevance": 0.142857,
    "complexity": 0.142857,
    "technical_depth": 0.142857,
    "domain_relevance": 0.142857,
    "execution_quality": 0.142857
}

def calculate_weighted_score(metrics: dict) -> float:
    total_score = 0
    total_weight = 0
    for metric, weight in WEIGHTS.items():
        if metric in metrics:
            total_score += metrics[metric] * weight
            total_weight += weight
    return round(total_score / total_weight, 3) if total_weight > 0 else 0.0

def process_resume(json_path: Path):
    if json_path.name == "example_output.json":
        return None
    try:
        with json_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"⚠️ Skipping invalid JSON: {json_path}")
        return None

    candidate_name = data.get("name", "Unknown")
    projects = data.get("projects", [])
    if not projects:
        aggregate_score = 0.0
    else:
        project_scores = [calculate_weighted_score(p.get("metrics", {})) for p in projects]
        aggregate_score = round(sum(project_scores) / len(project_scores), 3)

    return {"name": candidate_name, "project_aggregate": aggregate_score}

def main():
    results = []
    json_files = sorted(PROCESSED_JSON_DIR.glob("*.json"))
    for json_file in json_files:
        result = process_resume(json_file)
        if result:
            results.append(result)
            # print(f"✅ Processed {result['name']} | Project Aggregate: {result['project_aggregate']}")

    # Load existing scores
    if OUTPUT_FILE.exists():
        with OUTPUT_FILE.open("r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    # Build existing map for update
    existing_map = {r["name"]: r for r in existing_data if isinstance(r, dict)}
    for r in results:
        existing_map[r["name"]] = r

    updated_scores = list(existing_map.values())
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(updated_scores, f, indent=4)

    print(f"\n📂 All results written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
