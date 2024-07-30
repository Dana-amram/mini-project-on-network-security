import "./App.css";
import { ThemeProvider } from "@mui/material";
import theme from "./theme";
import SurveyDescription from "./components/SurveyDescription";
import SurveyForm from "./components/SurveyForm";

function App() {
  return (
    <div className="App">
      <ThemeProvider theme={theme}>
        <SurveyDescription />
        <SurveyForm />
      </ThemeProvider>
    </div>
  );
}

export default App;
