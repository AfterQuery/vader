import React from 'react'

import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Form from './Pages/Form';
import Multiform from './Pages/Multiform';
import Upload from './Components/Upload';
const App = () => {
  return (
    <div>
      <Router>
        <Routes>
          <Route path='/form' element={<Form />} />
          <Route path='/check' element={<Multiform />} />
          <Route path='/upload' element={<Upload />} />
        </Routes>
      </Router>
    </div>
  )
}

export default App