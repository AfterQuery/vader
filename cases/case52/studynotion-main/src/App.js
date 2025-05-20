import "./App.css";
import { Navbar } from './components/Navbar';
import { PrivateRoute } from './components/PrivateRoute';
import {Route,Routes } from "react-router-dom";
import { Home } from "./pages/Home";
import {Dashboard} from "./pages/Dashboard";
import {Login} from "./pages/Login";
import { Signup} from "./pages/Signup";
import { useState } from "react";

function App() {
  const [isLoggedIn, setIsLoggedIn]= useState(false);
  return (
    <div className="w-screen min-h-screen bg-richblack-900 flex flex-col">
      <Navbar  isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn}/>
      <Routes>
        <Route path="/" element={<Home  isLoggedIn={isLoggedIn}  />} />
       
        <Route path="/Login" element={<Login setIsLoggedIn={setIsLoggedIn} />} />
        <Route path="/Signup" element={<Signup setIsLoggedIn={setIsLoggedIn} />} />
        <Route path="/Dashboard" element={
          <PrivateRoute isLoggedIn={isLoggedIn}>
         <Dashboard />
          </PrivateRoute>
          
          } />
      </Routes>
    </div>
  );
}

export default App;
