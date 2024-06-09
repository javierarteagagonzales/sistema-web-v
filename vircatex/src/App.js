import React from 'react'
import {Routes, Route, BrowserRouter} from "react-router-dom"
import Home from "./pages/Home"
import A1 from "./pages/A1"
import A2 from "./pages/A2"
import A3 from "./pages/A3"
import A4 from "./pages/A4"
import A5 from "./pages/A5"
import A6 from "./pages/A6"
import A7 from "./pages/A7"

// Acabados
import AcabadoPage from './pages/acabados/acabados';
import LotesPage from './pages/acabados/lotes';

// Almacén Central
import SolicitudPage from './pages/almacencentral/solicitud';
import EstadoInvPage from './pages/almacencentral/estado-inv';
import EstadoPage from './pages/almacencentral/estado';
import ResumenPage from './pages/almacencentral/resumen';


// Calidad
import Tipo1Page from './pages/calidad/tipo-1';
import Tipo2Page from './pages/calidad/tipo-2';
import Tipo3Page from './pages/calidad/tipo-3';

// Confección
import GuiaPage from './pages/confeccion/guia';
import OrdenConfeccionPage from './pages/confeccion/orden';
import PlanPage from './pages/confeccion/plan';

// Corte
import DetallePage from './pages/corte/detalle';
import OrdenCortePage from './pages/corte/orden';

// PCP
import ControlarPage from './pages/pcp/controlar';
import EstadoPage1 from './pages/pcp/estado';
import ProgramarPage from './pages/pcp/programar';

// Tránsito
import Transito1Page from './pages/transito/1';
import Transito2Page from './pages/transito/2';
import Transito3Page from './pages/transito/3';



export default function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" exact element={<Home />}></Route>
          <Route path="/area1" exact element={<A1 />}></Route>
          <Route path="/area2" exact element={<A2 />}></Route>
          <Route path="/area3" exact element={<A3 />}></Route>
          <Route path="/area4" exact element={<A4 />}></Route>
          <Route path="/acabados" exact element={<A5 />}></Route>
          <Route path="/area6" exact element={<A6 />}></Route>
          <Route path="/area7" exact element={<A7 />}></Route>


          {/* Almacén Central */}
          <Route path="/acabados/acabados" element={<AcabadoPage />} />
          <Route path="/acabados/lotes" element={<LotesPage />} />

          {/* Almacén Central */}
          <Route path="/almacencentral/solicitud" element={<SolicitudPage />} />
          <Route path="/almacencentral/estado-inv" element={<EstadoInvPage />} />
          <Route path="/almacencentral/estado" element={<EstadoPage />} />
          <Route path="/almacencentral/resumen" element={<ResumenPage />} />
        
        {/* Calidad */}
        <Route path="/calidad/tipo-1" element={<Tipo1Page />} />
        <Route path="/calidad/tipo-2" element={<Tipo2Page />} />
        <Route path="/calidad/tipo-3" element={<Tipo3Page />} />

        {/* Confección */}
        <Route path="/confeccion/guia" element={<GuiaPage />} />
        <Route path="/confeccion/orden" element={<OrdenConfeccionPage />} />
        <Route path="/confeccion/plan" element={<PlanPage />} />
        
        {/* Corte */}
        <Route path="/corte/detalle" element={<DetallePage />} />
        <Route path="/corte/orden" element={<OrdenCortePage />} />
        
        {/* PCP */}
        <Route path="/pcp/controlar" element={<ControlarPage />} />
        <Route path="/pcp/estado" element={<EstadoPage1 />} />
        <Route path="/pcp/programar" element={<ProgramarPage />} />
        
        {/* Tránsito */}
        <Route path="/transito/1" element={<Transito1Page />} />
        <Route path="/transito/2" element={<Transito2Page />} />
        <Route path="/transito/3" element={<Transito3Page />} />

        </Routes>
      </BrowserRouter>
    </>
  )
}
