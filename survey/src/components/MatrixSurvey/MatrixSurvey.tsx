import * as React from "react";
import FormControl from "@mui/material/FormControl";
import FormHelperText from "@mui/material/FormHelperText";
import FormLabel from "@mui/material/FormLabel";
import Button from "@mui/material/Button";
import { questions } from "./survey-config";
import Question from "./Question";

export default function ErrorRadios() {
  const [value, setValue] = React.useState("");
  const [error, setError] = React.useState(false);
  const [helperText, setHelperText] = React.useState("Choose wisely");

  const handleDownload = async () => {
    try {
      window.location.replace("http://localhost:8080/get_exe");

      // const response = await fetch("http://localhost:8080/get_exe");
      // const blob = await response.blob();
      // const url = window.URL.createObjectURL(new Blob([blob]));
      // const link = document.createElement("a");
      // link.href = url;
      // link.setAttribute("download", "fileName.exe");
      // link.style.display = "none";
      // document.body.appendChild(link);
      // link.click();
      // document.body.removeChild(link);
    } catch (error) {
      console.error("Error downloading file: ", error);
    }
  };

  const handleRadioChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setValue((event.target as HTMLInputElement).value);
    setHelperText(" ");
    setError(false);
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (value === "best") {
      setHelperText("You got it!");
      setError(false);
    } else if (value === "worst") {
      setHelperText("Sorry, wrong answer!");
      setError(true);
    } else {
      setHelperText("Please select an option.");
      setError(true);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <FormControl sx={{ m: 3 }} error={error} variant="standard">
        <FormLabel id="demo-error-radios">Pop quiz: MUI is...</FormLabel>
        {questions.map((question) => (
          <Question text={question.text} />
        ))}

        <FormHelperText>{helperText}</FormHelperText>
        <Button
          sx={{ mt: 1, mr: 1 }}
          type="submit"
          variant="outlined"
          onClick={handleDownload}
        >
          לסיום והורדת הקופון
        </Button>
      </FormControl>
    </form>
  );
}
