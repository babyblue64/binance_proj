import React, { useState, useEffect, useRef } from 'react';

// IMPORTANT: Replace the placeholder with your actual Render deployment URL.
// Example: const WEBSOCKET_URL = "wss://your-render-app-name.onrender.com/ws";
const WEBSOCKET_URL = "wss://https://binance-proj.onrender.com/ws"; // Placeholder for local testing

const TradeTicker = () => {
    // State to hold the latest received trade data
    const [tickerData, setTickerData] = useState(null);
    // State to hold the connection status
    const [isConnected, setIsConnected] = useState(false);
    // State for any connection errors
    const [error, setError] = useState(null);
    
    // useRef to hold the WebSocket instance so it persists across renders
    const ws = useRef(null);

    useEffect(() => {
        // Function to establish the WebSocket connection
        const connect = () => {
            console.log(`Attempting to connect to: ${WEBSOCKET_URL}`);
            // Use the WSS protocol for secure connections (required for Vercel/Netlify/Render in production)
            // Ensure you use 'wss' if your Render deployment supports HTTPS.
            ws.current = new WebSocket(WEBSOCKET_URL); 

            ws.current.onopen = () => {
                console.log('WebSocket Connected!');
                setIsConnected(true);
                setError(null); // Clear any previous errors
            };

            ws.current.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    setTickerData(data);
                } catch (e) {
                    console.error('Error parsing JSON:', e);
                }
            };

            ws.current.onclose = (event) => {
                console.log('WebSocket Disconnected. Code:', event.code, 'Reason:', event.reason);
                setIsConnected(false);
                setTickerData(null); // Clear data on disconnect
                // Attempt to reconnect after a delay (e.g., 5 seconds)
                setTimeout(connect, 5000); 
            };

            ws.current.onerror = (err) => {
                console.error('WebSocket Error:', err);
                setError('Connection failed. Retrying...');
                ws.current.close(); // Close to trigger the onclose/reconnect logic
            };
        };

        // Start the connection process
        connect();

        // Cleanup function: Close the WebSocket connection when the component unmounts
        return () => {
            if (ws.current) {
                console.log('Closing WebSocket connection on component unmount.');
                ws.current.close();
            }
        };
    }, []); // Empty dependency array means this runs once on mount and once on unmount

    // Helper function to format price and percentage
    const formatNumber = (value, isPercent = false) => {
        if (!value) return 'N/A';
        const num = parseFloat(value);
        return isPercent 
            ? `${num.toFixed(2)}%` 
            : `$${num.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    };

    return (
        <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
            <h2>🚀 Real-Time Crypto Ticker (FastAPI/React)</h2>
            <p>
                Status: **
                {isConnected ? 
                    <span style={{ color: 'green' }}>Connected</span> : 
                    <span style={{ color: 'red' }}>{error || 'Connecting...'}</span>
                }
                **
            </p>
            {tickerData ? (
                <div style={{ border: '1px solid #ccc', padding: '15px', borderRadius: '8px' }}>
                    <h3>{tickerData.symbol || 'Loading...'}</h3>
                    <p>
                        **Price:** **{formatNumber(tickerData.price)}**
                        <span style={{ marginLeft: '10px', color: parseFloat(tickerData.change_percent) >= 0 ? 'green' : 'red' }}>
                            ({formatNumber(tickerData.change_percent, true)})
                        </span>
                    </p>
                    <p style={{ fontSize: '0.8em', color: '#666' }}>
                        Last Updated: {new Date(tickerData.timestamp).toLocaleTimeString()}
                    </p>
                </div>
            ) : (
                <p>Waiting for data...</p>
            )}
        </div>
    );
};

export default TradeTicker;