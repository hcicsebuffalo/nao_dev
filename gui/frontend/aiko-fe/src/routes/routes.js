import React, { useEffect, createContext, useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import App from '../App';
import Camera from '../components/global/camera';

export const SettingsContext = createContext();

export function Routing() {                                                                      //routes for the project

    return (
        // <SettingsContext.Provider value={[settings, testSettings]}>
        <div>
            <Routes>
                <Route path="/" exact  element={<Camera />} />
            </Routes>
        </div>
        // </SettingsContext.Provider>

    )
}