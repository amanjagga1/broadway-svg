import requests
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_variant_map(tgid: str) -> Tuple[Optional[List[str]], Optional[Dict[str, int]]]:
    variant_map: Dict[str, int] = {}
    variant_names: List[str] = []
    tour_groups_url = f'https://www.headout.com/api/v6/tour-groups/{tgid}'
    inventories_url = (
        f'https://www.headout.com/api/v7/tour-groups/{tgid}/inventories'
        f'?from-date={datetime.now().strftime("%Y-%m-%d")}&to-date=2025-12-12'
    )

    try:
        with ThreadPoolExecutor() as executor:
            # Run the fetch_data calls concurrently
            future_to_url = {
                executor.submit(fetch_data, inventories_url): 'inventories',
                executor.submit(fetch_data, tour_groups_url): 'tour_groups'
            }

            inventories_data = None
            tour_groups_data = None

            for future in as_completed(future_to_url):
                url_type = future_to_url[future]
                try:
                    data = future.result()
                    if url_type == 'inventories':
                        inventories_data = data
                    elif url_type == 'tour_groups':
                        tour_groups_data = data
                except Exception as e:
                    print(f"Error fetching {url_type} data: {e}")

            # Process inventories data
            active_variants = set()
            if inventories_data:
                active_variants = {availability['tourId'] for availability in inventories_data.get('availabilities', [])}

            # Process tour groups data
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
    """Fetch SVG concurrently with the other API calls."""

    special_tgids = {
        "27108", "740", "25948", "25637", "12525", "10069", "29103", 
        "24867", "24863", "28796", "29141", "29075", "29100", "1963", 
        "28594", "29398", "29400", "29399", "30012"
    }

    if tgid in special_tgids:
        url = f'https://tourlandish.s3.amazonaws.com/custom-broadway-svg/hifi-seatmaps/{tgid}.svg'
    else:
        url = f'https://tourlandish.s3.amazonaws.com/lofi-seatmaps/{tgid}.svg'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"SVG fetch failed for {tgid}: {e}")
        return None