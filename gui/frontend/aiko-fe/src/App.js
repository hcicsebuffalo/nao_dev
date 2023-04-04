import React, { createContext } from 'react';
import logo from './logo.svg';
import './App.css';

import { BrowserRouter as Router,
  Route } from 'react-router-dom';
import { Routing } from './routes/routes';
import history from './services/history'
// import { login } from './components/login';

export const SettingsContext = createContext();


export class App extends React.Component {
  render(){
    return (
      <div>
        <Router history={history}>
          <Routing />
        </Router>
      </div>
    );
  } 
}

export default App;