// vendor imports
import { createGlobalStyle } from "styled-components";

const globalStyle = createGlobalStyle`
  html, body, #root {
    margin: 0;
    width: 100%;
    height: 100%;

    background-image: linear-gradient(135deg, #fdfcfb 0%, #e2d1c3 100%);
  }

  #root {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
`;

export default globalStyle;
