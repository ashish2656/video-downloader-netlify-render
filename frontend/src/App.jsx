import { useEffect, useMemo, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";

const STATUS_STYLES = {
  idle: "",
  downloading: "status status--info",
  completed: "status status--success",
  error: "status status--error"
};

const API_BASE = import.meta.env.VITE_API_BASE || "";

export default function App() {
  const [url, setUrl] = useState("");
  const [choice, setChoice] = useState("video");
  const [status, setStatus] = useState({ type: "idle", message: "" });
  const [taskId, setTaskId] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState("");

  const canSubmit = useMemo(() => url.trim().length > 0 && !isSubmitting, [url, isSubmitting]);

  useEffect(() => {
    if (!taskId) {
      return undefined;
    }

    let cancelled = false;
    let attempts = 0;
    const interval = setInterval(async () => {
      if (cancelled) {
        return;
      }
      attempts += 1;
      try {
        const response = await fetch(`${API_BASE}/api/status/${taskId}`);
        const data = await response.json();

        if (data.status === "downloading") {
          setStatus({
            type: "downloading",
            message: data.message || "Preparing download"
          });
        }

        if (data.status === "completed") {
          const urlFromApi = data.download_url || "";
          const resolvedUrl = urlFromApi.startsWith("http")
            ? urlFromApi
            : `${API_BASE}${urlFromApi}`;
          setStatus({
            type: "completed",
            message: data.title || "Request accepted"
          });
          setDownloadUrl(resolvedUrl);
          setIsSubmitting(false);
          clearInterval(interval);
        }

        if (data.status === "error") {
          setStatus({
            type: "error",
            message: data.message || "Something went wrong"
          });
          setDownloadUrl("");
          setIsSubmitting(false);
          clearInterval(interval);
        }

        if (attempts >= 60) {
          setStatus({
            type: "error",
            message: "Request timed out. Try again."
          });
          setDownloadUrl("");
          setIsSubmitting(false);
          clearInterval(interval);
        }
      } catch (error) {
        setStatus({ type: "error", message: "Network error. Try again." });
        setDownloadUrl("");
        setIsSubmitting(false);
        clearInterval(interval);
      }
    }, 1000);

    return () => {
      cancelled = true;
      clearInterval(interval);
    };
  }, [taskId]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!url.trim()) {
      setStatus({ type: "error", message: "Please enter a URL." });
      setDownloadUrl("");
      return;
    }

    setIsSubmitting(true);
    setStatus({ type: "downloading", message: "Submitting request" });
    setDownloadUrl("");

    try {
      const response = await fetch(`${API_BASE}/api/download`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url, choice })
      });

      const data = await response.json();
      if (!response.ok) {
        setStatus({ type: "error", message: data.error || "Request failed" });
        setDownloadUrl("");
        setIsSubmitting(false);
        return;
      }

      setTaskId(data.task_id);
    } catch (error) {
      setStatus({ type: "error", message: "Network error. Try again." });
      setDownloadUrl("");
      setIsSubmitting(false);
    }
  };

  return (
    <div className="page">
      <div className="glow" aria-hidden="true" />
      <motion.main
        className="card"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
      >
        <motion.header
          className="header"
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1, duration: 0.5 }}
        >
          <p className="eyebrow">Instant media toolkit</p>
          <h1>Video Downloader</h1>
          <p className="subtitle">
            Clean, fast requests for YouTube and Instagram downloads. Hosted on Render, delivered via Netlify.
          </p>
        </motion.header>

        <form className="form" onSubmit={handleSubmit}>
          <label className="field">
            <span>Video URL</span>
            <input
              type="url"
              placeholder="https://www.youtube.com/watch?v=..."
              value={url}
              onChange={(event) => setUrl(event.target.value)}
              required
            />
          </label>

          <div className="field">
            <span>Download format</span>
            <div className="choice-row">
              {[
                { value: "video", label: "Video" },
                { value: "audio", label: "Audio" },
                { value: "both", label: "Both" }
              ].map((option) => (
                <label key={option.value} className={choice === option.value ? "choice choice--active" : "choice"}>
                  <input
                    type="radio"
                    name="choice"
                    value={option.value}
                    checked={choice === option.value}
                    onChange={() => setChoice(option.value)}
                  />
                  <span>{option.label}</span>
                </label>
              ))}
            </div>
          </div>

          <button type="submit" className="primary" disabled={!canSubmit}>
            {isSubmitting ? "Sending request" : "Start download"}
          </button>
        </form>

        <AnimatePresence mode="wait">
          {status.type !== "idle" && (
            <motion.section
              key={status.type}
              className={STATUS_STYLES[status.type]}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.25 }}
            >
              <div className="status__indicator" aria-hidden="true" />
              <div>
                <p className="status__title">{status.type}</p>
                <p className="status__message">{status.message}</p>
                {status.type === "completed" && downloadUrl ? (
                  <a className="status__action" href={downloadUrl}>
                    Download file
                  </a>
                ) : null}
              </div>
            </motion.section>
          )}
        </AnimatePresence>

        <footer className="footer">
          <div>
            <p>Render API</p>
            <span>{API_BASE ? API_BASE : "Set VITE_API_BASE"}</span>
          </div>
          <div>
            <p>Netlify</p>
            <span>Static UI build</span>
          </div>
        </footer>
      </motion.main>
    </div>
  );
}
