import { useState } from "react";
import { useGoogleLogin } from "@react-oauth/google";
import { signInWithCustomToken, signOut } from "firebase/auth";
import { auth } from "./firebase";
import { fetchCustomToken } from "./api";
import "./App.css";

function App() {
  const [uid, setUid] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const login = useGoogleLogin({
    flow: "auth-code",
    scope: "openid",
    onSuccess: async (response) => {
      setLoading(true);
      setError(null);

      try {
        const { custom_token, uid: anonymizedUid } = await fetchCustomToken(
          response.code
        );
        await signInWithCustomToken(auth, custom_token);
        setUid(anonymizedUid);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Authentication failed"
        );
      } finally {
        setLoading(false);
      }
    },
    onError: () => setError("Google login failed"),
  });

  const handleLogout = async () => {
    await signOut(auth);
    setUid(null);
    setError(null);
  };

  return (
    <div className="container">
      <h1>Google SSO + Firebase Custom Auth</h1>
      <p className="description">
        Privacy-first authentication: your Google account ID is anonymized via
        HMAC-SHA256 before being stored in Firebase.
      </p>

      {loading && <p className="status">Authenticating...</p>}
      {error && <p className="error">{error}</p>}

      {uid ? (
        <div className="result">
          <p className="label">Authenticated!</p>
          <p className="uid-label">Anonymized UID:</p>
          <code className="uid">{uid}</code>
          <button className="logout" onClick={handleLogout}>
            Logout
          </button>
        </div>
      ) : (
        !loading && (
          <div className="login">
            <button className="google-login" onClick={() => login()}>
              Sign in with Google
            </button>
          </div>
        )
      )}
    </div>
  );
}

export default App;
