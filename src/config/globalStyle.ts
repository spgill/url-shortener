// vendor imports
import { createGlobalStyle } from "styled-components";

const globalStyle = createGlobalStyle`
  html, body, #root {
    margin: 0;
    width: 100%;
    height: 100%;

    background-color: #FAACA8;
    background-image: linear-gradient(45deg, #FAACA8 0%, #DDD6F3 100%);
  }

  #root {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
`;

export default globalStyle;
