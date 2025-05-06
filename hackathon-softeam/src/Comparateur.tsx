import React from 'react';
import Navbar from './components/Navbar';
import ApexChart from './components/column-chart';

const Comparateur: React.FC = () => {
  return (
    <div>
      <Navbar />
      <main style={{ marginTop: '100px' }}>
        <ApexChart />
      </main>
      <Footer />
    </div>
  );
};

const Footer = () => (
    <footer>
      <p>HACKATON - 2025 - SOFTEAM</p>
    </footer>
  );

export default Comparateur;