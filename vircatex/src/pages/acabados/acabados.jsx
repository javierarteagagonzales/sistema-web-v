import React from 'react'
import Sidenav from '../../components/Sidenav'
import Navbar from '../../components/Navbar'
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { useState } from 'react';
import '../../App.css';

//navegation
import Navigation from "../../components/Navigation";
import Home from "../Home";
import A5 from "../A5";

export default function AcabadoPage() {
/* popup */
const [showPopup, setShowPopup] = useState(false);

const togglePopup = () => {
  setShowPopup(!showPopup);
};

  return (
    <>
    <Navbar />
    <Box height={30}/>
    <Box sx={{ display: 'flex' }}>
      <Sidenav/>
      
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
       <h1>Área de Acabados</h1> 
       <div>
        <Navigation />
        
      </div>

        <Typography paragraph>
          resumen
        </Typography>

        <div className="App1">
      <button onClick={togglePopup}>Mostrar Popup</button>
      {showPopup && (
        <div className="overlay">
          <div className="popup">
            <button onClick={togglePopup}>Cerrar Popup</button>
            <h2>Este es un Popup</h2>
            <p>Contenido del popup...</p>
          </div>
        </div>
      )}
    </div>


      </Box>

    </Box>
      
    
      
    </>
  )
}