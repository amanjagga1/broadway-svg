import requests
from datetime import datetime
from typing import Dict, List, Tuple, Optional

def fetch_variant_map(tgid: str) -> Tuple[Optional[List[str]], Optional[Dict[str, int]]]:
    variant_map: Dict[str, int] = {}
    variant_names: List[str] = []
    tour_groups_url = f'https://www.headout.com/api/v6/tour-groups/{tgid}'
    inventories_url = (
        f'https://www.headout.com/api/v7/tour-groups/{tgid}/inventories'
        f'?from-date={datetime.now().strftime("%Y-%m-%d")}&to-date=2025-12-12'
    )
    active_variants = set()

    try:
        # Fetch inventories
        inventories_data = fetch_data(inventories_url)
        if inventories_data:
            active_variants = {availability['tourId'] for availability in inventories_data.get('availabilities', [])}

        # Fetch tour group data
        tour_groups_data = fetch_data(tour_groups_url)
        if tour_groups_data:
            for variant in tour_groups_data.get('variants', []):
                tour = variant.get('tours', [{}])[0]
                variant_name = tour.get('variantName')
                tour_id = tour.get('id')

                if variant_name and tour_id in active_variants:
                    if variant_name not in variant_names:
                        variant_names.append(variant_name)
                        variant_map[variant_name] = tour_id

        return variant_names, variant_map

    except requests.RequestException as e:
        print(f"Error fetching variant map: {e}")
        return None, None

def fetch_data(url: str) -> Optional[dict]:
    """Helper function to handle GET requests and return JSON response."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Request failed for {url}: {e}")
        return None
    
def fetch_svg(tgid: str):
    try:
        response = requests.get(f'https://tourlandish.s3.amazonaws.com/lofi-seatmaps/{tgid}.svg')
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"SVG fetch failed for {tgid}: {e}")
        return None