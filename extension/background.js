console.log("🔗 [SW] starting up");
let port = null,
  attempt = 0;

function connect() {
  attempt++;
  console.log(`🔌 [SW] Attempt ${attempt}: connectNative…`);
  if (port) {
    port.disconnect();
    port = null;
  }
  port = chrome.runtime.connectNative("com.nativebridge.test");
  port.onMessage.addListener((msg) => {
    console.log("[SW] ‹message›", msg);
    if (msg.type === "ahk_event") {
      console.log("✅ [SW] AHK event:", msg.payload);
    } else if (msg.echo) {
      console.log("✅ [SW] Echo from Python:", msg.echo);
    }
  });
  port.onDisconnect.addListener(() => {
    console.warn("[SW] disconnected", chrome.runtime.lastError);
    setTimeout(connect, 1000);
  });
  console.log(`📝 [SW] sending handshake`);
  port.postMessage({ cmd: "start", attempt });
}

connect();
