#!/usr/bin/env python3
"""
Test script to check the analytics API endpoint with authentication
"""

import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_analytics_api_with_auth():
    """Test the analytics API endpoint with authentication"""
    try:
        # Create a session to maintain cookies
        session = requests.Session()
        
        # First, try to login (using existing user credentials)
        login_data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        
        print("Attempting to login...")
        login_response = session.post('http://127.0.0.1:5000/login', data=login_data)
        print(f"Login response status: {login_response.status_code}")
        
        # Now try to access the analytics API
        print("Attempting to access analytics API...")
        api_response = session.get('http://127.0.0.1:5000/api/analytics-data')
        print(f"API response status: {api_response.status_code}")
        
        if api_response.status_code == 200:
            try:
                data = api_response.json()
                print("API Response Data:")
                print(f"  Status: {data.get('status')}")
                print(f"  Hotspots count: {len(data.get('hotspots', []))}")
                if 'hotspots' in data:
                    for i, hotspot in enumerate(data['hotspots']):
                        print(f"    {i+1}. {hotspot.get('city')}: {hotspot.get('cases')} cases, risk {hotspot.get('level')}")
                print(f"  Last updated: {data.get('last_updated')}")
            except Exception as e:
                print(f"Error parsing JSON: {e}")
                print(f"Response content: {api_response.text[:500]}...")
        else:
            print(f"API request failed with status {api_response.status_code}")
            print(f"Response headers: {api_response.headers}")
            print(f"Response content: {api_response.text[:500]}...")
            
    except Exception as e:
        print(f"❌ Error testing analytics API with auth: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_analytics_api_with_auth()