# Public Transport Optimization - Recommendations Report

## Executive Summary
Based on the analysis of NYC Subway and Bus data, we have identified three key areas for optimization to improve efficiency and passenger experience.

## 1. Peak Hour Frequency Adjustment
**Recommendation**: Increase subway frequency during **7-9 AM** and **5-7 PM**.

**Data Evidence**:
- Analysis of `cleaned_subway.csv` shows a distinct spike in ridership during these hours.
- Current ridership levels during these peaks suggest potential overcrowding.
- **Action**: Deploy additional trains on high-volume lines (e.g., lines serving Manhattan business districts) during these windows.

## 2. Bus Lane Implementation in Congested Boroughs
**Recommendation**: Implement dedicated bus lanes in boroughs with lower average speeds, specifically **Manhattan**.

**Data Evidence**:
- `bus_speeds.csv` analysis reveals that Manhattan has the lowest average bus speeds compared to other boroughs.
- The boxplot `plots/bus_speed_by_borough.png` clearly illustrates this disparity.
- **Action**: Work with DOT to designate bus-only lanes on major crosstown and avenue routes in Manhattan to improve speed and reliability.

## 3. Service Adjustments for Low Ridership Stations
**Recommendation**: Monitor and potentially adjust service for stations with consistently low ridership.

**Data Evidence**:
- Granular station-level data indicates significant variance in utilization.
- **Action**: Conduct a station-by-station audit. For stations falling below a certain ridership threshold off-peak, consider increasing headways (time between trains) to save operational costs without significantly impacting service quality.

## Conclusion
Implementing these data-driven strategies is projected to reduce overcrowding, improve bus commute times, and optimize operational resource allocation.
