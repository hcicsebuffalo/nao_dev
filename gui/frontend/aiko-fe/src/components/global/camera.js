import React, { useEffect, useState } from 'react'
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Unstable_Grid2';
import axios from 'axios'
import logo from '../../logo.svg';
import '../../App.css';

const Camera = () => {
  return (
    <div style={{ padding: '1%' }}>
      <Box sx={{ flexGrow: 1 }}>
        <Grid container spacing={2}>
          <Grid xs={6} >
            <div>
              <h1>Video Feed</h1>
              <img
                src="http://127.0.0.1:8000/api/getfeed"
                alt="Video"
                style={{ height: '500px', width: '680px', padding: "2%"}}
              />
            </div>
          </Grid>
          <Grid xs={6}>
            <div>
              <h1>Chats</h1>
            </div>
          </Grid>
          <Grid xs={6}>
            <div>
              <h1>Choose Actions</h1>
            </div>
          </Grid>
          <Grid xs={6}>
            <div>
              <h1>Sensors</h1>
            </div>
          </Grid>
        </Grid>
      </Box>
      
    </div>
  );
};
export default Camera;