import { useState } from "react";
import {
  Alert,
  AppBar,
  Box,
  Button,
  CircularProgress,
  Container,
  Divider,
  Paper,
  TextField,
  Toolbar,
  Typography,
} from "@mui/material";
import PictureAsPdfIcon from "@mui/icons-material/PictureAsPdf";
import UploadFileIcon from "@mui/icons-material/UploadFile";
import SendIcon from "@mui/icons-material/Send";

import {
  askQuestion,
  uploadPdf,
  type ChatSource,
} from "./services/api";

function App() {
  const [documentId, setDocumentId] = useState("");
  const [fileName, setFileName] = useState("");

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState<ChatSource[]>([]);

  const [uploading, setUploading] = useState(false);
  const [asking, setAsking] = useState(false);

  const [error, setError] = useState("");

  const handleFileChange = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    setError("");
    setUploading(true);

    try {
      const result = await uploadPdf(file);

      setDocumentId(result.document_id);
      setFileName(result.filename);

      setQuestion("");
      setAnswer("");
      setSources([]);
    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : "Failed to upload PDF.";

      setError(message);
    } finally {
      setUploading(false);
    }
  };

  const handleAskQuestion = async () => {
    if (!question.trim()) {
      return;
    }

    if (!documentId) {
      setError("Please upload a PDF first.");
      return;
    }

    setError("");
    setAsking(true);

    try {
      const result = await askQuestion(
        question,
        documentId
      );

      setAnswer(result.answer);
      setSources(result.sources);
    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : "Failed to get an answer.";

      setError(message);
    } finally {
      setAsking(false);
    }
  };

  const handleQuestionKeyDown = (
    event: React.KeyboardEvent
  ) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleAskQuestion();
    }
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        backgroundColor: "#f5f7fa",
      }}
    >
      <AppBar position="static" elevation={0}>
        <Toolbar>
          <PictureAsPdfIcon sx={{ mr: 1 }} />

          <Typography
            variant="h6"
            component="div"
            sx={{ fontWeight: 600 }}
          >
            Chat with Your PDF
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="md" sx={{ py: 6 }}>
        <Box sx={{ textAlign: "center", mb: 5 }}>
          <Typography
            variant="h3"
            component="h1"
            sx={{
              fontWeight: 700,
              mb: 2,
            }}
          >
            Chat with Your PDF
          </Typography>

          <Typography
            variant="h6"
            color="text.secondary"
            sx={{ fontWeight: 400 }}
          >
            Upload a document and ask questions using
            AI-powered retrieval.
          </Typography>
        </Box>

        <Paper
          elevation={2}
          sx={{
            p: 5,
            textAlign: "center",
            borderRadius: 3,
          }}
        >
          <UploadFileIcon
            sx={{
              fontSize: 64,
              mb: 2,
              color: "primary.main",
            }}
          />

          <Typography
            variant="h5"
            sx={{
              fontWeight: 600,
              mb: 1,
            }}
          >
            Upload your PDF
          </Typography>

          <Typography
            color="text.secondary"
            sx={{ mb: 3 }}
          >
            Choose a PDF document to start asking
            questions.
          </Typography>

          <Button
            variant="contained"
            size="large"
            component="label"
            startIcon={
              uploading ? (
                <CircularProgress
                  size={20}
                  color="inherit"
                />
              ) : (
                <UploadFileIcon />
              )
            }
            disabled={uploading}
          >
            {uploading ? "Uploading..." : "Choose PDF"}

            <input
              type="file"
              accept=".pdf,application/pdf"
              hidden
              onChange={handleFileChange}
            />
          </Button>

          {fileName && (
            <Alert
              severity="success"
              sx={{
                mt: 3,
                textAlign: "left",
              }}
            >
              <strong>{fileName}</strong>{" "}
              uploaded successfully.
            </Alert>
          )}
        </Paper>

        <Paper
          elevation={1}
          sx={{
            mt: 4,
            p: 4,
            borderRadius: 3,
          }}
        >
          <Typography
            variant="h5"
            sx={{
              fontWeight: 600,
              mb: 1,
            }}
          >
            Ask questions about your document
          </Typography>

          <Typography
            color="text.secondary"
            sx={{ mb: 3 }}
          >
            {documentId
              ? "Your document is ready. Ask a question below."
              : "Upload a PDF to start the conversation."}
          </Typography>

          <TextField
            fullWidth
            multiline
            minRows={2}
            maxRows={5}
            placeholder="Ask something about your PDF..."
            value={question}
            onChange={(event) =>
              setQuestion(event.target.value)
            }
            onKeyDown={handleQuestionKeyDown}
            disabled={!documentId || asking}
          />

          <Box
            sx={{
              display: "flex",
              justifyContent: "flex-end",
              mt: 2,
            }}
          >
            <Button
              variant="contained"
              endIcon={
                asking ? (
                  <CircularProgress
                    size={18}
                    color="inherit"
                  />
                ) : (
                  <SendIcon />
                )
              }
              onClick={handleAskQuestion}
              disabled={
                !documentId ||
                !question.trim() ||
                asking
              }
            >
              {asking ? "Thinking..." : "Ask"}
            </Button>
          </Box>

          {answer && (
            <Box sx={{ mt: 4 }}>
              <Divider sx={{ mb: 3 }} />

              <Typography
                variant="h6"
                sx={{
                  fontWeight: 600,
                  mb: 2,
                }}
              >
                Answer
              </Typography>

              <Paper
                variant="outlined"
                sx={{
                  p: 3,
                  backgroundColor: "#fafafa",
                }}
              >
                <Typography
                  sx={{
                    whiteSpace: "pre-wrap",
                    lineHeight: 1.7,
                  }}
                >
                  {answer}
                </Typography>
              </Paper>

              {sources.length > 0 && (
                <Box sx={{ mt: 3 }}>
                  <Typography
                    variant="subtitle1"
                    sx={{
                      fontWeight: 600,
                      mb: 1,
                    }}
                  >
                    Sources
                  </Typography>

                  {sources.map((source) => (
                    <Paper
                      key={source.chunk_id}
                      variant="outlined"
                      sx={{
                        p: 2,
                        mb: 1,
                      }}
                    >
                      <Typography
                        variant="body2"
                        sx={{ fontWeight: 600 }}
                      >
                        Page {source.page}
                      </Typography>

                      <Typography
                        variant="body2"
                        color="text.secondary"
                      >
                        {source.text}
                      </Typography>
                    </Paper>
                  ))}
                </Box>
              )}
            </Box>
          )}
        </Paper>

        {error && (
          <Alert
            severity="error"
            sx={{ mt: 3 }}
          >
            {error}
          </Alert>
        )}
      </Container>
    </Box>
  );
}

export default App;