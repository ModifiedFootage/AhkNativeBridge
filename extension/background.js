console.log("🔗 [SW] starting up");

function connect() {
  console.log("🔌 [SW] connecting to native host…");
  const port = chrome.runtime.connectNative("com.nativebridge.test");

  port.onMessage.addListener((msg) => {
    console.log("📨 [SW] AHK event:", msg.event);
  });

  port.onDisconnect.addListener(() => {
    console.warn("⚠️ [SW] native port disconnected", chrome.runtime.lastError);
    // try to reconnect in 1 s
    setTimeout(connect, 1000);
  });

  console.log("📝 [SW] sending handshake");
  port.postMessage({ cmd: "start" });
}

// fire immediately when the SW spins up:
connect();
