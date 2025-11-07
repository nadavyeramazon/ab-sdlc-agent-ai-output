import React from 'react';
import styled from 'styled-components';

const AppContainer = styled.div`
  min-height: 100vh;
  background-color: #d4edda;
  color: #155724;
  display: flex;
  justify-content: center;
  align-items: center;
`;

const App = () => {
  return (
    &lt;AppContainer>
      &lt;h1>Welcome to the Green Themed UI&lt;/h1>
    &lt;/AppContainer>
  );
};

export default App;
