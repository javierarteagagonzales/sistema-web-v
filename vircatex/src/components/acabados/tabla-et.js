import React from 'react'




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


  function createData(name, code, population, size) {
    return { name, code, population, size, };
  }
  
  const rows = [
    createData('India', 'IN', 13, 32),
  
  ];

  const columns = [
    { id: 'name', label: 'Prenda', minWidth: 100 },
    { id: 'code', label: 'ID\u00a0Confección', minWidth: 100 },
    { id: 'population',label: 'Medida', minWidth: 100,},
    { id: 'size', label: 'Estilo\u00a0Prenda', minWidth: 100,  },
    { id: 'population1',label: 'Talla', minWidth: 100,},
    { id: 'population2',label: 'Género', minWidth: 100,},
    { id: 'population3',label: 'Estado', minWidth: 100,},
  ];


  export default function DenseTable() {
    return (
  <Paper sx={{ width: '100%' }}>
  <TableContainer sx={{ maxHeight: 200 }} component={Paper}>
    <Table sx={{ minWidth: 650 }} size="small" aria-label="a dense table">
      <TableHead>
        <StyledTableRow>
        <StyledTableCell rowSpan={2}>Prenda</StyledTableCell>
        <StyledTableCell rowSpan={2}>IDConfección</StyledTableCell>
        <StyledTableCell align="center" colSpan={7}>Medida</StyledTableCell>
        <StyledTableCell align="right" rowSpan={2}>Estilo</StyledTableCell>
        <StyledTableCell align="right" rowSpan={2}>Talla</StyledTableCell>
        <StyledTableCell align="right" rowSpan={2}>Género</StyledTableCell>
        <StyledTableCell align="right" rowSpan={2}>Estado</StyledTableCell>

        </StyledTableRow>
        <StyledTableRow>
        <StyledTableCell align="right">ml</StyledTableCell>
        <StyledTableCell align="right">mh</StyledTableCell>
        <StyledTableCell align="right">mp</StyledTableCell>
        <StyledTableCell align="right">mm</StyledTableCell>
        <StyledTableCell align="right">mc</StyledTableCell>
        <StyledTableCell align="right">mca</StyledTableCell>
        <StyledTableCell align="right">mmu</StyledTableCell>
      </StyledTableRow>
        
      </TableHead>
      <TableBody>
        {rows
          
          .map((row) => {
            return (
              <TableRow hover role="checkbox" tabIndex={-1} key={row.code}>
                {columns.map((column) => {
                  const value = row[column.id];
                  return (
                    <TableCell key={column.id} align={column.align}>
                      {column.format && typeof value === 'number'
                        ? column.format(value)
                        : value}
                    </TableCell>
                  );
                })}
              </TableRow>
            );
          })}
      </TableBody>
    </Table>
  </TableContainer>
  
</Paper>

);
}