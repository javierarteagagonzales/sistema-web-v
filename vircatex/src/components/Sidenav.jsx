import * as React from 'react';
import { styled, useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import MuiDrawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import CssBaseline from '@mui/material/CssBaseline';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';

import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';

import HomeIcon from '@mui/icons-material/Home';
import InventoryIcon from '@mui/icons-material/Inventory';
import ContentCutIcon from '@mui/icons-material/ContentCut';
import CheckroomIcon from '@mui/icons-material/Checkroom';
import DirectionsTransitIcon from '@mui/icons-material/DirectionsTransit';
import EngineeringIcon from '@mui/icons-material/Engineering';
import GradingIcon from '@mui/icons-material/Grading';
import DeveloperBoardIcon from '@mui/icons-material/DeveloperBoard';
import { useNavigate } from 'react-router-dom';
import { useAppStore } from '../appStore';
import MenuItem from './MenuItem';

const drawerWidth = 300;

const openedMixin = (theme) => ({
  width: drawerWidth,
  transition: theme.transitions.create('width', {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.enteringScreen,
  }),
  overflowX: 'hidden',
});

const closedMixin = (theme) => ({
  transition: theme.transitions.create('width', {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  overflowX: 'hidden',
  width: `calc(${theme.spacing(7)} + 1px)`,
  [theme.breakpoints.up('sm')]: {
    width: `calc(${theme.spacing(8)} + 1px)`,
  },
});

const DrawerHeader = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'flex-end',
  padding: theme.spacing(0, 1),
  ...theme.mixins.toolbar,
}));

const Drawer = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    width: drawerWidth,
    flexShrink: 0,
    whiteSpace: 'nowrap',
    boxSizing: 'border-box',
    ...(open && {
      ...openedMixin(theme),
      '& .MuiDrawer-paper': openedMixin(theme),
    }),
    ...(!open && {
      ...closedMixin(theme),
      '& .MuiDrawer-paper': closedMixin(theme),
    }),
  }),
);

export default function Sidenav() {
  const theme = useTheme();
  const navigate = useNavigate();
  const updateOpen = useAppStore((state) => state.updateOpen);
  const open = useAppStore((state) => state.dopen);

  const handleDrawerToggle = () => {
    updateOpen(!open);
  };

  const menuItems = [
    {
      text: 'Home',
      icon: <HomeIcon />,
      path: '/',
      subItems: []
    },
    {
      text: 'Almacén Central',
      icon: <InventoryIcon />,
      path: '/area1',
      subItems: [
        { text: 'Resumen', path: '/almacencentral/resumen' },
        { text: 'Solicitud', path: '/almacencentral/solicitud' },
        { text: 'Estado', path: '/almacencentral/estado' },
        { text: 'Estado inventario', path: '/almacencentral/estado-inv' },
      ]
    },
    {
      text: 'Corte',
      icon: <ContentCutIcon />,
      path: '/area2',
      subItems: [
        { text: 'Detalles de lote', path: '/corte/detalle' },
        { text: 'Órdenes de trabajo', path: '/corte/orden' },
      ]
    },
    {
      text: 'Confección',
      icon: <CheckroomIcon />,
      path: '/area3',
      subItems: [
        { text: 'Orden de trabajo', path: '/confeccion/orden' },
        { text: 'Plan de confección', path: '/confeccion/plan' },
        { text: 'Guía de confección', path: '/confeccion/guia' },
      ]
    },
    {
      text: 'Almacén de tránsito',
      icon: <DirectionsTransitIcon />,
      path: '/area4',
      subItems: [
        { text: '1', path: '/transito/1' },
        { text: '2', path: '/transito/2' },
        { text: '3', path: '/transito/3' },
      ]
    },
    {
      text: 'Acabados',
      icon: <EngineeringIcon />,
      path: '/acabados',
      subItems: [
        { text: 'Lotes', path: '/acabados/lotes' },
        { text: 'Acabados', path: '/acabados/acabados' },
      ]
    },
    {
      text: 'Inspección de Calidad',
      icon: <GradingIcon />,
      path: '/area6',
      subItems: [
        { text: 'Tipo 1', path: '/calidad/tipo-1' },
        { text: 'Tipo 2', path: '/calidad/tipo-2' },
        { text: 'Tipo 3', path: '/calidad/tipo-3' },
      ]
    },
    {
      text: 'PCP',
      icon: <DeveloperBoardIcon />,
      path: '/area7',
      subItems: [
        { text: 'Programar producción', path: '/pcp/programar' },
        { text: 'Controlar producción', path: '/pcp/controlar' },
        { text: 'Estado de proveedores', path: '/pcp/estado' },
      ]
    },
  ];

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <Box height={30} />
      <Drawer variant="permanent" open={open}>
        <DrawerHeader>
          <IconButton onClick={handleDrawerToggle}>
            {theme.direction === 'rtl' ? <ChevronRightIcon /> : <ChevronLeftIcon />}
          </IconButton>
        </DrawerHeader>
        <Divider />
        <List>
          {menuItems.map((item, index) => (
            <MenuItem key={index} item={item} navigate={navigate} open={open} />
          ))}
        </List>
      </Drawer>
    </Box>
  );
}
