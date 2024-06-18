from fastapi import Query, HTTPException
from datetime import timedelta
from sqlalchemy import func
from ..models.sensor import SensorData
from ..utills.helpers import get_latest_timestamp

def get_sensor_data(params):
    valid_statistics = {"min", "max", "sum", "average"}
    valid_metrics = {"temperature", "humidity", "pressure", "wind_speed"}

    # Validate statistics
    if params['statistics']:
        for stat in params['statistics']:
            if stat not in valid_statistics:
                raise HTTPException(status_code=400, detail=f"Invalid statistic: {stat}")

    # Validate metrics
    if params['metrics']:
        for metric in params['metrics']:
            if metric not in valid_metrics:
                raise HTTPException(status_code=400, detail=f"Invalid metric: {metric}")

    query = params['db'].query(SensorData)

    # Filter by sensor_id if provided
    if params['sensor_ids']:
        query = query.filter(SensorData.sensor_id.in_(params['sensor_ids']))

    # Determine the date range
    if params['start_date'] and params['end_date']:
        if params['end_date'] < params['start_date']:
            raise HTTPException(status_code=400, detail="End date must be after start date")
        query = query.filter(SensorData.timestamp >= params['start_date'],
                             SensorData.timestamp <= params['end_date'])
    elif params['start_date'] and not params['end_date']:
        query = query.filter(SensorData.timestamp >= params['start_date'])
    elif not params['start_date'] and params['end_date']:
        query = query.filter(SensorData.timestamp <= params['end_date'])
    else:
        # If no date range is provided, use the latest date
        latest_timestamp = get_latest_timestamp(params['db'])
        
        # Default to the last 7 days (a week)
        params['start_date'] = latest_timestamp - timedelta(days=7)
        query = query.filter(SensorData.timestamp >= params['start_date'],
                             SensorData.timestamp <= latest_timestamp)

    try:
        results = query.all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while querying data: {str(e)}")

    # Compute statistics if the statistics parameter is provided
    stats = {}
    if params['statistics'] and params['metrics']:
        stats_query = {}
        stats_keys = []
        for metric in params['metrics']:
            for statistic in params['statistics']:
                if statistic == "min":
                    stats_query[f"{metric}_min"] = func.min(getattr(SensorData, metric))
                elif statistic == "max":
                    stats_query[f"{metric}_max"] = func.max(getattr(SensorData, metric))
                elif statistic == "sum":
                    stats_query[f"{metric}_sum"] = func.sum(getattr(SensorData, metric))
                elif statistic == "average":
                    stats_query[f"{metric}_avg"] = func.avg(getattr(SensorData, metric))
                stats_keys.append(f"{metric}_{statistic}")

        stats_query = params['db'].query(*stats_query.values()).filter(
            SensorData.timestamp >= params['start_date'],
            SensorData.timestamp <= (params['end_date']
                                     if params['end_date'] else latest_timestamp))

        # Filter by sensor_ids if provided
        if params['sensor_ids']:
            stats_query = stats_query.filter(SensorData.sensor_id.in_(params['sensor_ids']))

        try:
            stat_results = stats_query.one()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while querying statistics: {str(e)}")

        # Prepare the statistics dictionary
        for key, result in zip(stats_keys, stat_results):
            if "avg" or "sum" in key:
                stats[key] = round(result, 4)
            else:
                stats[key] = result

    # Convert results to dictionaries and add statistics at the end
    results_dicts = [result.__dict__ for result in results]
    if params['statistics'] and params['metrics']:
        results_dicts.append({"metrics": stats})
    
    return results_dicts