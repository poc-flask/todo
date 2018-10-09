"""Test health API endpoint"""
import requests


def test_healthz_endpoint(client):
    """Make sure the service health api works fine."""
    rv = client.get('/healthz', follow_redirects=True)

    assert rv.status_code == requests.codes.ok
