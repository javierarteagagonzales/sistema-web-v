import React from 'react'
import Sidenav from '../../components/Sidenav'
import Navbar from '../../components/Navbar'
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

import { useEffect, useState } from 'react';
import { getAllData } from '../../api/v.api'

// tablas
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell, { tableCellClasses } from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

//estilos
import { styled } from '@mui/material/styles';

//navegation
import Navigation from "../../components/Navigation";
import A5 from "../A5";

const StyledTableCell = styled(TableCell)(({ theme }) => ({
  [`&.${tableCellClasses.head}`]: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  [`&.${tableCellClasses.body}`]: {
    fontSize: 10,
  },
}));

const StyledTableRow = styled(TableRow)(({ theme }) => ({
  '&:nth-of-type(odd)': {
    backgroundColor: theme.palette.action.hover,
  },
  // hide last border
  '&:last-child td, &:last-child th': {
    border: 0,
  },
}));


export default function LotesPage() {
const [acabado, setAcabado] = useState([]);


useEffect(() => {
  async function loadData() {
    const res = await getAllData();
    setAcabado(res.data);
  }
  loadData();
},[]);

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
          Resumen
        </Typography>
        
        <div>
        {/*<h1>{acabado.id}</h1>
        <p>{acabado.nombre}</p>
        
        <table border="1">
          <tr>
          <td>{acabado.id}</td>
          <td>{acabado.nombre}</td>
          </tr>
        </table>*/}
        <TableContainer component={Paper}>
          <Table sx={{ maxWidth: 500 }} aria-label="simple table">
            <TableHead>
              <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Nombre</TableCell>
              <TableCell>Fecha</TableCell>
              <TableCell>Caja Entrada</TableCell>
              <TableCell>Caja Salida</TableCell>
              </TableRow>
              </TableHead>
              <TableBody>
              {acabado.map(acabado => (
              <StyledTableRow >
              <StyledTableCell >{acabado.id}</StyledTableCell>
              <StyledTableCell >{acabado.nombre}</StyledTableCell>
              </StyledTableRow>
            ))}
              </TableBody>
            </Table>
        </TableContainer>
        
        
        </div> 
       

      </Box>
      
    </Box>
      
    
      
    </>
  )
}