# 📊 Analytics & Monitoring Extensions

## Overview

The Analytics & Monitoring Extensions module provides comprehensive fraud analytics, real-time anomaly detection, and financial impact estimation capabilities for the Multi-Domain Fraud Detection Platform (MDFDP).

## Features

### A. Fraud Heatmaps
Interactive geographical visualization of fraud density across India with the following capabilities:

#### Key Features:
- **Interactive Map**: Satellite view with fraud hotspot markers
- **Filtering Options**: Filter by fraud type (UPI, Credit Card, Phishing, Identity Theft)
- **Risk Levels**: Visual indicators for Critical, High, Medium, and Low risk zones
- **Real-time Statistics**:
  - Total Cases (24h)
  - Critical Zones Count
  - Average Severity
  - 24-hour Trend

#### Cities Monitored:
- Mumbai (Critical)
- Delhi (High)
- Bangalore (Medium)
- Hyderabad (High)
- Kolkata (Medium)
- Chennai (Low)
- Pune (Medium)
- Ahmedabad (Medium)
- And 12 more cities across India

### B. Anomaly Detection Dashboard
Real-time monitoring of anomalies across all fraud detection channels.

#### Key Features:
- **Live Activity Feed**: Real-time anomaly alerts with severity levels
- **Auto-refresh**: Updates every 10 seconds
- **Anomaly Statistics**:
  - Active Anomalies Count
  - Critical Anomalies
  - Resolved Anomalies (24h)
  - Average Response Time
- **Trend Visualization**: Interactive chart showing anomaly patterns over 24 hours
- **Severity Classification**: Critical, High, Medium, Low

#### Detected Anomaly Types:
- UPI Fraud
- Suspicious Login Attempts
- Credit Card Blocks
- Identity Verification Failures
- Phishing Attempts
- Account Takeovers
- Unusual Transaction Patterns
- Bot Activity
- Data Breach Attempts
- Fake Profile Creation

### C. Fraud Loss Estimation Tool
Predict financial damage under different attack scenarios.

#### Configuration Parameters:
1. **Attack Type**:
   - UPI Fraud
   - Credit Card Fraud
   - Phishing Campaign
   - Identity Theft
   - Ransomware
   - DDoS Attack

2. **Attack Scale**:
   - Small (1-100 targets)
   - Medium (100-1,000 targets)
   - Large (1,000-10,000 targets)
   - Massive (10,000+ targets)

3. **Transaction Details**:
   - Average Transaction Value (₹)
   - Estimated Success Rate (%)
   - Attack Duration (hours)
   - Detection Delay (minutes)

#### Financial Impact Analysis:
The tool calculates:
- **Direct Loss**: Immediate financial damage from successful attacks
- **Indirect Costs**: Recovery expenses, legal fees (30% of direct loss)
- **Reputational Damage**: Brand impact based on attack type
- **Total Estimated Loss**: Comprehensive financial impact
- **Affected Users**: Number of users impacted
- **Risk Level**: Overall risk classification

#### Recommendations Engine:
Provides customized security recommendations based on:
- Risk level (Critical/High/Medium/Low)
- Detection delay
- Attack type specific measures

## Access

Navigate to the Analytics & Monitoring dashboard:
- **URL**: `/analytics`
- **Navigation**: Click "Analytics" in the main navigation menu
- **Authentication**: Login required

## Technical Implementation

### Frontend:
- **HTML/CSS**: Modern, responsive design with dark theme
- **JavaScript**: Interactive features with Chart.js and Leaflet.js
- **Libraries**:
  - Leaflet.js (v1.9.4) - Interactive maps
  - Chart.js - Data visualization
  - Font Awesome (v6.4.0) - Icons

### Backend:
- **Framework**: Flask
- **Route**: `/analytics` (GET)
- **Authentication**: `@login_required` decorator

### Files:
- `templates/analytics_dashboard.html` - Main dashboard template
- `static/js/analytics.js` - JavaScript functionality
- `app.py` - Flask route definition

## Usage Guide

### 1. Viewing Fraud Heatmaps:
1. Navigate to Analytics dashboard
2. Default view shows all fraud types
3. Click filter buttons to view specific fraud types
4. Hover over markers for detailed information
5. View statistics below the map

### 2. Monitoring Anomalies:
1. Click "Anomaly Detection" tab
2. View real-time anomaly feed (auto-refreshes)
3. Check severity badges (Critical, High, Medium, Low)
4. Review anomaly statistics and trends
5. Monitor the 24-hour trend chart

### 3. Estimating Fraud Loss:
1. Click "Loss Estimation" tab
2. Fill in the attack scenario form:
   - Select attack type
   - Choose attack scale
   - Enter average transaction value
   - Set success rate percentage
   - Specify attack duration
   - Input detection delay
3. Click "Calculate Loss Estimation"
4. Review financial impact analysis
5. Read customized recommendations

## Data Visualization

### Color Coding:
- **Critical**: Red (#d50000)
- **High**: Orange (#ff6f00)
- **Medium**: Yellow (#f9a825)
- **Low**: Green (#2e7d32)

### Interactive Elements:
- Hover effects on all cards
- Smooth transitions and animations
- Responsive design for mobile devices
- Custom scrollbars for lists

## Security Considerations

- All routes protected with authentication
- No sensitive data exposed in client-side code
- Simulated data for demonstration purposes
- Real implementation should connect to actual fraud detection systems

## Future Enhancements

1. **Real-time Data Integration**: Connect to live fraud detection systems
2. **Historical Analysis**: Add time-range selectors for historical data
3. **Export Functionality**: Download reports as PDF/CSV
4. **Alert Configuration**: Customizable alert thresholds
5. **Multi-region Support**: Expand beyond India
6. **Predictive Analytics**: ML-based fraud prediction
7. **Comparative Analysis**: Compare fraud patterns across regions/time periods
8. **Integration with Detection Modules**: Direct links to specific fraud detection modules

## Performance Optimization

- Lazy loading of map tiles
- Efficient DOM manipulation
- Debounced event handlers
- Optimized chart rendering
- Minimal API calls

## Browser Compatibility

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Troubleshooting

### Map Not Loading:
- Check internet connection
- Verify Leaflet.js CDN is accessible
- Clear browser cache

### Charts Not Displaying:
- Ensure Chart.js is loaded
- Check browser console for errors
- Verify canvas element exists

### Data Not Updating:
- Check auto-refresh interval (10 seconds)
- Verify JavaScript is enabled
- Check for console errors

## Support

For issues or questions:
- Check the main MDFDP documentation
- Review browser console for errors
- Ensure all dependencies are loaded
- Verify authentication status

## Credits

- **Maps**: Leaflet.js with Esri World Imagery
- **Charts**: Chart.js
- **Icons**: Font Awesome
- **Design**: Custom dark theme with gradient accents

---

**Last Updated**: November 28, 2025
**Version**: 1.0.0
**Module**: Analytics & Monitoring Extensions
