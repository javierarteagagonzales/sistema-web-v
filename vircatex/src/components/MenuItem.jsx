import React, { useState } from 'react';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Collapse from '@mui/material/Collapse';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import List from '@mui/material/List';

export default function MenuItem({ item, navigate, open }) {
  const [subOpen, setSubOpen] = useState(false);

  const handleClick = () => {
    if (item.subItems.length > 0) {
      setSubOpen(!subOpen);
    } else {
      navigate(item.path);
    }
  };

  return (
    <>
      <ListItem disablePadding sx={{ display: 'block' }} onClick={handleClick}>
        <ListItemButton
          sx={{
            minHeight: 48,
            justifyContent: open ? 'initial' : 'center',
            px: 2.5,
            fontWeight: 'bold',
            fontSize: '16px',
            color: '#000',
          }}
        >
          <ListItemIcon
            sx={{
              minWidth: 0,
              mr: open ? 3 : 'auto',
              justifyContent: 'center',
              color: 'inherit',
            }}
          >
            {item.icon}
          </ListItemIcon>
          <ListItemText primary={item.text} sx={{ opacity: open ? 1 : 0 }} />
          {item.subItems.length > 0 ? (subOpen ? <ExpandLess /> : <ExpandMore />) : null}
        </ListItemButton>
      </ListItem>
      {item.subItems.length > 0 && (
        <Collapse in={subOpen} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            {item.subItems.map((subItem, subIndex) => (
              <ListItem key={subIndex} disablePadding sx={{ pl: 4 }}>
                <ListItemButton
                  sx={{
                    maxHeight: 32,
                    justifyContent: open ? 'initial' : 'center',
                    px: 4,
                    fontSize: '10px',
                    color: '#555555',
                  }}
                  onClick={() => navigate(subItem.path)}
                >
                  <ListItemText primary={subItem.text} sx={{ opacity: open ? 1 : 0 }} />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </Collapse>
      )}
    </>
  );
}
