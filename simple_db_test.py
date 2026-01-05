#!/usr/bin/env python3
"""
Simple test script to check the database and data processing logic
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db_connection

def test_database_and_processing():
    """Test the database query and data processing logic"""
    try:
        # Test the database query directly
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT module_name, fraud_probability, risk_level, timestamp
            FROM fraud_analysis_logs
            ORDER BY timestamp DESC
            LIMIT 10
        ''')
        records = cursor.fetchall()
        conn.close()
        
        print(f"✅ Retrieved {len(records)} recent fraud analysis records:")
        for i, record in enumerate(records):
            print(f"  {i+1}. {record['module_name']} - Probability: {record['fraud_probability']}, Risk: {record['risk_level']}")
            
        # Test the processing logic from app.py
        print("\n🔄 Testing data processing logic...")
        
        module_stats = {}
        risk_levels = {'LOW': 0, 'MEDIUM': 0, 'HIGH': 0, 'CRITICAL': 0}
        
        for record in records:
            module_name = record['module_name']
            if module_name not in module_stats:
                module_stats[module_name] = {'count': 0, 'fraud_cases': 0, 'total_probability': 0}
            
            module_stats[module_name]['count'] += 1
            module_stats[module_name]['total_probability'] += record['fraud_probability'] or 0
            
            # Count fraud cases (probability > 0.5)
            if (record['fraud_probability'] or 0) > 0.5:
                module_stats[module_name]['fraud_cases'] += 1
            
            # Update risk level statistics
            risk_level = (record['risk_level'] or 'UNKNOWN').upper()
            if risk_level in risk_levels:
                risk_levels[risk_level] += 1
            else:
                risk_levels['LOW'] += 1  # Default to low for unknown
        
        print(f"📊 Module statistics:")
        for module_name, stats in module_stats.items():
            avg_prob = stats['total_probability'] / stats['count'] if stats['count'] > 0 else 0
            fraud_rate = (stats['fraud_cases'] / stats['count']) * 100 if stats['count'] > 0 else 0
            print(f"  {module_name}: {stats['count']} analyses, {stats['fraud_cases']} fraud cases, {avg_prob:.2f} avg prob, {fraud_rate:.1f}% fraud rate")
            
        print(f"🚨 Risk level distribution: {risk_levels}")
        
        # Test the conversion to heatmap format
        print("\n🗺️ Testing heatmap data conversion...")
        
        # City coordinates mapping (simplified)
        city_coords = {
            'Unknown': [22.9734, 78.6569]  # Center of India
        }
        
        # Convert to format expected by frontend heatmap
        hotspots = []
        for module_name, stats in module_stats.items():
            if stats['count'] > 0:
                avg_probability = stats['total_probability'] / stats['count']
                fraud_rate = (stats['fraud_cases'] / stats['count']) * 100
                
                # Determine risk level based on fraud rate
                if fraud_rate >= 20:
                    level = 'critical'
                elif fraud_rate >= 10:
                    level = 'high'
                elif fraud_rate >= 5:
                    level = 'medium'
                else:
                    level = 'low'
                
                # Use module name as "city" for visualization
                hotspots.append({
                    'city': module_name,
                    'coords': city_coords.get('Unknown', [22.9734, 78.6569]),
                    'level': level,
                    'cases': stats['count'],
                    'types': {
                        'upi': stats['count'] if 'UPI' in module_name else 0,
                        'credit': stats['count'] if 'Credit' in module_name else 0,
                        'phishing': stats['count'] if 'Phishing' in module_name else 0,
                        'identity': stats['count'] if 'Profile' in module_name or 'Identity' in module_name else 0
                    }
                })
        
        print(f"📍 Generated {len(hotspots)} heatmap hotspots:")
        for hotspot in hotspots:
            print(f"  {hotspot['city']}: {hotspot['cases']} cases, risk level {hotspot['level']}")
            
        return hotspots
        
    except Exception as e:
        print(f"❌ Error testing database and processing: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    hotspots = test_database_and_processing()
    print(f"\n✅ Test completed. Generated {len(hotspots)} heatmap hotspots.")