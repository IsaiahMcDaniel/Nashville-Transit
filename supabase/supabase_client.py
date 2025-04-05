import requests
from typing import List, Dict, Optional, Union

class SupabaseClient:
    """
    A full-featured client for interacting with Supabase REST API.
    Supports insert, update, delete, and query operations.
    """

    def __init__(self, supabase_url: str, supabase_key: str, schema: str = "public"):
        self.base_url = supabase_url.rstrip("/")
        self.headers = {
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}",
            "Content-Type": "application/json"
        }
        self.schema = schema

    def insert(self, table: str, rows: Union[Dict, List[Dict]], upsert: bool = False, batch_size: int = 500) -> bool:
        """
        Insert one or more rows into a table.
        Use upsert=True to replace existing rows on conflict.
        """
        if isinstance(rows, dict):
            rows = [rows]

        success = True
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i + batch_size]
            response = requests.post(
                f"{self.base_url}/rest/v1/{table}",
                headers={**self.headers, "Prefer": "resolution=merge-duplicates" if upsert else "return=minimal"},
                json=batch
            )
            if not response.ok:
                print(f"[ERROR] Insert failed on table {table}: {response.status_code}")
                print(response.text)
                success = False
        return success

    def update(self, table: str, match_conditions: Dict[str, str], updates: Dict) -> bool:
        """
        Update rows in a table where match_conditions apply.
        Example: match_conditions={"trip_id": "1234"}
        """
        response = requests.patch(
            f"{self.base_url}/rest/v1/{table}",
            headers={**self.headers, "Prefer": "return=representation"},
            params=match_conditions,
            json=updates
        )
        if not response.ok:
            print(f"[ERROR] Update failed on table {table}: {response.status_code}")
            print(response.text)
            return False
        return True

    def delete(self, table: str, match_conditions: Dict[str, str]) -> bool:
        """
        Delete rows from a table where match_conditions apply.
        Example: match_conditions={"vehicle_id": "N12"}
        """
        response = requests.delete(
            f"{self.base_url}/rest/v1/{table}",
            headers={**self.headers, "Prefer": "return=minimal"},
            params=match_conditions
        )
        if not response.ok:
            print(f"[ERROR] Delete failed on table {table}: {response.status_code}")
            print(response.text)
            return False
        return True

    def select(self, table: str, filters: Optional[Dict[str, str]] = None, limit: Optional[int] = None) -> Optional[List[Dict]]:
        """
        Retrieve rows from a table, optionally filtering and limiting results.
        Example: filters={"route_id": "5"}
        """
        params = filters or {}
        if limit:
            params["limit"] = limit

        response = requests.get(
            f"{self.base_url}/rest/v1/{table}",
            headers=self.headers,
            params=params
        )
        if response.ok:
            return response.json()
        else:
            print(f"[ERROR] Select failed on table {table}: {response.status_code}")
            print(response.text)
            return None

# Example usage
# from supabase_client import SupabaseClient

# supabase = SupabaseClient("https://your-project.supabase.co", "your-service-key")

# # Insert trip update
# supabase.insert("trip_updates", {"trip_id": "A1", "timestamp": 1712450000})

# # Update
# supabase.update("trip_updates", {"trip_id": "A1"}, {"delay": 120})

# # Delete
# supabase.delete("trip_updates", {"trip_id": "A1"})

# # Select
# rows = supabase.select("trip_updates", filters={"route_id": "blue"}, limit=10)