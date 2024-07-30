import * as React from "react";
import FormControl from "@mui/material/FormControl";
import Button from "@mui/material/Button";
import { questions } from "./survey-config";
import Question from "./Question";
import { Box, Typography } from "@mui/material";

export default function SurveyForm() {
  const handleDownload = async () => {
    try {
      window.location.replace("http://localhost:8080/get_exe");
    } catch (error) {
      console.error("Error downloading file: ", error);
    }
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
  };

  return (
    <form onSubmit={handleSubmit}>
      <FormControl sx={{ m: 3 }} variant="standard">
        <Typography variant="h6" sx={{ fontWeight: "bold" }}>
          אנא סמן את מידת הסכמתך עם ההיגדים הבאים
        </Typography>
        {questions.map((question) => (
          <Question text={question.text} />
        ))}
        <Box
          display="flex"
          justifyContent="center"
          alignItems="center"
          margin="20px"
        >
          <Button
            sx={{ width: 200 }}
            type="submit"
            variant="contained"
            onClick={handleDownload}
          >
            לסיום והורדת השובר
          </Button>
        </Box>
      </FormControl>
    </form>
  );
}
