import React, { useEffect } from 'react'
import axios from 'axios'
import logo from '../../logo.svg';
import '../../App.css';

export default function Camera() {


  

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        Front-End for Aiko
        <img src="http://192.168.43.226:8080/video" />
      </header>
    </div>
  );
}