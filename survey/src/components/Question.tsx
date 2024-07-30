import * as React from "react";
import Radio from "@mui/material/Radio";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import { options } from "./survey-config";

export default function Question({ text }: { text: string }) {
  const [value, setValue] = React.useState("1");

  const handleRadioChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setValue((event.target as HTMLInputElement).value);
  };

  return (
    <div>
      <RadioGroup
        aria-labelledby="demo-error-radios"
        name="quiz"
        value={value}
        onChange={handleRadioChange}
      >
        <p>{text}</p>
        {options.map((option) => (
          <FormControlLabel
            value={option.value}
            control={<Radio />}
            label={option.text}
          />
        ))}
      </RadioGroup>
    </div>
  );
}
