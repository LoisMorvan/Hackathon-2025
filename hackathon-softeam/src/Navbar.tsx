import React from 'react';
import './Navbar.css'; 

const Navbar = () => (
  <nav className="navbar">
    <ul className="nav-links">
      <li><a href="/">Accueil</a></li>
      <li><a href="/comparateur">Comparateur</a></li>
      <li><a href="/situation">Situation</a></li>
    </ul>
  </nav>
);

export default Navbar;