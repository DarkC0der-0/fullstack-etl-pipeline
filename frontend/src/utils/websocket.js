const wsUrl = "ws://localhost:8000/ws/etl_status";
let ws;

const connect = (onMessageCallback) => {
  ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    console.log("Connected to WebSocket");
  };

  ws.onmessage = (event) => {
    onMessageCallback(event.data);
  };

  ws.onerror = (error) => {
    console.error("WebSocket error:", error);
  };

  ws.onclose = (event) => {
    console.error("WebSocket closed:", event);
    setTimeout(() => connect(onMessageCallback), 5000); // Reconnect after 5 seconds
  };
};

export const onMessage = (callback) => {
  connect(callback);
};