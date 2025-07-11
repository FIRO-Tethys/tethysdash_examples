from datetime import datetime, timedelta
from sodapy import Socrata


def run_query(borough, start_date, end_date):
    """Run a query to get car theft data for the specified borough and date range."""
    client = Socrata("data.cityofnewyork.us", None)

    start_date_object = datetime.strptime(start_date, "%m/%d/%Y")
    end_date_object = datetime.strptime(end_date, "%m/%d/%Y")
    # Format the dates for the query
    start_date = start_date_object.strftime("%Y-%m-%d")
    end_date = end_date_object.strftime("%Y-%m-%d")

    # Container to hold all results that the API returns
    all_results = []
    # Form the where clause for the query to filter by borough and date range
    where_clause = f"boro_nm='{borough.upper()}' AND cmplnt_fr_dt BETWEEN '{start_date}' AND '{end_date}'"

    # Initial offset for the API query
    offset = 0
    while True:
        # Get the next 2000 results
        api_response = client.get(
            "a9pz-ixz5", limit=2000, offset=offset, where=where_clause
        )
        # Break if no more results are returned
        if not api_response:
            break
        # Add the results to the container
        all_results.extend(api_response)
        # Increment the offset to get the next 2000 results
        offset += 2000

    # Format the results for a JSON response
    results = {"results": []}
    for result in all_results:
        results["results"].append(
            {
                "borough": result["boro_nm"].capitalize(),
                "time": result["cmplnt_fr_tm"],
                "date": datetime.strptime(
                    result["cmplnt_fr_dt"].split("T")[0], "%Y-%m-%d"
                ).strftime("%m/%d/%Y"),
                "latitude": result["latitude"],
                "longitude": result["longitude"],
            }
        )

    return results
