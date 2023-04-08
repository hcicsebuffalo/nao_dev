import React, { useEffect, useState } from 'react'
import axios from 'axios'
import logo from '../../logo.svg';
import '../../App.css';

const Camera = () => {
  return (
    <div>
      <img
        src="http://127.0.0.1:8000/api/getfeed"
        alt="Video"
      />
    </div>
  );
};
export default Camera;