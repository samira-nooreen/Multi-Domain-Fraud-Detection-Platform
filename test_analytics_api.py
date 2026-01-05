#!/usr/bin/env python3
"""
Test script to check the analytics API endpoint directly
"""

import requests
import json

def test_analytics_api():
    """Test the analytics API endpoint"""
    try:
        # Since this requires authentication, we'll simulate a simple test
        # by calling the function directly
        
        # Import the app and test function
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from app import analytics_data
        from database import get_user_by_email
        
        # Get a user for testing
        user = get_user_by_email('admin@example.com')  # Assuming this user exists
        if not user:
            print("❌ No test user found")
            return
            
        print(f"✅ Found user: {user['email']}")
        
        # Test the analytics data function
        print("📊 Testing analytics_data function...")
        
        # We can't directly call the Flask route function without proper context
        # So let's test the database query directly
        
        from database import get_db_connection
        
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
        
    except Exception as e:
        print(f"❌ Error testing analytics API: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_analytics_api()