// vendor imports
// import axios from "axios";
import { Button, Grommet, TextInput, Card, CardBody } from "grommet";
import { LinkDown } from "grommet-icons";
import React, { useCallback } from "react";
import styled from "styled-components";

// local imports
import theme from "../config/theme";

const ModifiedGrommet = styled(Grommet)`
  display: grid;
  /* grid-row-gap: 12px; */
  align-items: center;
`;

const CardBodyGrid = styled(CardBody)`
  display: grid;
  justify-items: center;

  row-gap: calc(${(theme) => theme.theme.global.spacing} / 2);

  > * {
    width: 100%;
  }
`;

function App() {
  // State vars
  const [inputValue, setInputValue] = React.useState("");
  const [outputValue, setOutputValue] = React.useState("");
  const [isPageLoading, setPageLoading] = React.useState(false);
  const [errorText, setErrorText] = React.useState<string>("");

  const handleInputChange: React.ChangeEventHandler<HTMLInputElement> =
    useCallback((ev) => {
      setInputValue(ev.target.value);
      setOutputValue("");
      setErrorText("");
    }, []);

  const handleClickSubmit = useCallback(async () => {
    setPageLoading(true);
    setErrorText("");

    try {
      const response = await fetch("/api", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: inputValue }),
      });

      if (!response.ok) {
        throw Error(response.statusText);
      }

      setOutputValue(await response.text());
    } catch (err) {
      setErrorText("Error shortening URL");
    }

    setPageLoading(false);
  }, [inputValue]);

  const handleClickCopy = useCallback(() => {
    if (outputValue) {
      navigator.clipboard.writeText(outputValue);
    }
  }, [outputValue]);

  return (
    <ModifiedGrommet theme={theme}>
      <Card background="light-1">
        <CardBodyGrid pad="medium">
          <TextInput
            placeholder="URL goes here"
            value={inputValue}
            onChange={handleInputChange}
            disabled={isPageLoading}
          />
          <Button
            primary={true}
            label="Shorten"
            onClick={handleClickSubmit}
            disabled={isPageLoading}
          />

          <LinkDown />

          {errorText ? (
            <p>{errorText}</p>
          ) : (
            <>
              <TextInput
                readOnly
                value={outputValue}
                disabled={isPageLoading}
              />
              <Button
                label="Copy to Clipboard"
                onClick={handleClickCopy}
                disabled={isPageLoading || !outputValue}
              />
            </>
          )}
        </CardBodyGrid>
      </Card>
    </ModifiedGrommet>
  );
}

export default App;
