import json
from typing import List, Dict

def analyze_search_gaps_and_schema(
    target_queries: List[Dict[str, str]],
    existing_pages: List[str],
    service_name: str,
    service_url: str,
) -> Dict[str, str]:
    # Identify high-intent content gaps without generating low-quality SEO spam
    existing_lower = ' '.join(existing_pages).lower()
    content_gaps = [
        q for q in target_queries
        if q['intent'] in {'commercial', 'transactional'} and q['keyword'].lower() not in existing_lower
    ]

    # Generate valid JSON-LD Structured Data for search engines
    json_ld = {
        '@context': 'https://schema.org',
        '@type': 'SoftwareApplication',
        'name': service_name,
        'url': service_url,
        'applicationCategory': 'BusinessApplication',
        'provider': {'@type': 'Organization', 'name': 'Cynbit'},
    }

    return {
        'prioritized_content_gaps': content_gaps,
        'structured_data_json_ld': json.dumps(json_ld, indent=2),
    }