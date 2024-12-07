'use client';
import React, { useEffect } from 'react';
import mapboxgl from 'mapbox-gl';

// Ensure Mapbox access token is set
mapboxgl.accessToken = process.env.NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN || '';

const FleetVision = () => {
  React.useEffect(() => {
    const map = new mapboxgl.Map({
      container: 'map',
      style: 'mapbox://styles/mapbox/streets-v11',
      center: [-74.5, 40], // Starting position [lng, lat]
      zoom: 9 // Starting zoom
    });

    return () => map.remove();
  }, []);

  return (
    <div style={{ display: 'flex', height: '100vh' }}>
      <div id="map" style={{ flex: 1 }}></div>
      <div style={{ flex: 1, borderLeft: '1px solid #ccc' }}>
        <h2>Chat Window</h2>
        {/* Chat window content will go here */}
      </div>
    </div>
  );
};

export default FleetVision;